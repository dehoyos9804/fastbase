# -*- coding: utf-8 -*-
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Generic
from typing import Union
from sqlmodel import SQLModel
from sqlmodel import Field
from sqlmodel import select
from contextlib import suppress
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as legacy_select
from sqlalchemy.orm.exc import NoResultFound
from loguru import logger

# Variable genérica para tipado
T = TypeVar("T", bound="GenericModel")


class GenericModel(SQLModel):
    """
    Modelo base abstracto con métodos CRUD asíncronos tipo ORM.
    Herada de SQLModel y añade funcionalidad común para interactuar con la base de datos de forma asíncrona.

    Las clases concretas deben heredar de esta y definir sus campos y opcionalmente `table=True`.
    """

    # Campo de ID común. Se puede sobreescribir en subclases si es necesario.
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description='Identificador único')

    async def save(self: T, session: AsyncSession) -> T:
        """
        Guarda (inserta o actualiza) la instancia actual en la base de datos

        - Si la instancia no tiene ID, la añade a la sesión (INSERT).
        - Si la instancia ya tiene ID, SQLAlchemy la manejará como UPDATE
          si ya está presente en la sesión o fue cargada desde ella.
        - Realiza un flush para asegurar que operaciones pendientes (como obtener el ID
          autogenerado) se ejecuten antes del commit (que ocurrirá fuera de este método).
        - Refresca la instancia para obtener cualquier valor actualizado desde la BD.

        Args:
            session (AsyncSession): La sesión de base de datos activa.

        Returns:
            T: La instancia guardada y refrescada.
        """
        try:
            session.add(self)
            # Envía operaciones pendientes a la BD (ejemplo: obtener ID)
            await session.flush()
            # Actualiza la instancia con datos de la BD
            await session.refresh(self)
            logger.info(f'Instancia {self.__class__.__name__}(id={self.id}) añadida/actualizada')
            return self
        except Exception as e:
            logger.error(f'Instancia {self.__class__.__name__}: {e}')
            # El rollback se manejará en el gestor de sesión
            raise

    async def update(self: T, session: AsyncSession, data: Dict[str, Any]) -> T:
        """
        Actualiza los campos de la instancia con datos de un diccionario.

        Solo actualiza los campos presentes en el diccionario `data` y que
        existen como atributos en el modelo. Luego llama a `save` para persistir.

        Args:
            session (AsyncSession): La sesión de base de datos activa.
            data (Dict[str, Any]): Diccionario con los campos y valores a actualizar.

        Returns:
            T: La instancia actualizada y guardada.
        """
        for key, value in data.items():
            # Verifica si el atributo existe en el modelo antes de asignarlo
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.info(f"Advertencia: El campo '{key}' no existe en el modelo {self.__class__.__name__} y será ignorado")

        # llama a save para persistir los cambios hechos por setattr
        return await self.save(session)

    async def delete(self, session: AsyncSession) -> None:
        """
        Elimina la instancia actual de la base de datos.

        Args:
            session (AsyncSession): La sesión de base de datos activa.
        """
        try:
            await session.delete(self)
            # Envía la operación DELETE a la BD
            await session.flush()
            logger.info(f'Instancia {self.__class__.__name__}(id={self.id}) marcada para eliminar en sesión')
        except Exception as e:
            logger.error(f'Error al eliminar {self.__class__.__name__}(id={self.id}): {e}')
            raise

    @classmethod
    async def get_by_id(
        cls: Type[T],
        session: AsyncSession,
        id: Any,
        as_dict: bool = False
    ) -> Optional[Union[T, Dict[str, Any]]]:
        """
        Obtiene una única instancia por su clave primaria (ID).

        Utiliza session.get para una búsqueda optimizada por PK.

        Args:
            session (AsyncSession): La sesión de base de datos activa.
            id (Any): El valor de la clave primaria a buscar.
            as_dict:
        Returns:
            T: La instancia encontrada.
        """
        try:
            result = await session.get(cls, id)
            if not result:
                logger.info(f'{cls.__name__} con id={id} no encontrado.')

            logger.info(f'{cls.__name__} con id={id} encontrado.')
            return result.model_dump() if as_dict else result
        except Exception as e:
            logger.error(f'Error al obtener {cls.__name__}(id={id}): {e}')
            raise

    @classmethod
    async def get_all(
        cls: Type[T],
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        as_dict: bool = False
    ) -> List[Union[T, Dict[str, Any]]]:
        """
        Obtiene una lista de todas las instancias con paginación opcional.

        Args:
            session (AsyncSession): La sesión de base de datos activa.
            skip (int): Número de registros a omitir (para paginación).
            limit (Optional[int]): Número máximo de registros a devolver. Si es None, devuelve todos.
            as_dict:
        Returns:
            List[T]: Lista de instancias encontradas.
        """
        try:
            statement = select(cls).offset(skip)

            if limit is not None:
                statement = statement.limit(limit)

            result = await session.execute(statement)
            instances = result.scalars().all()
            logger.info(f'Obtenidos {len(instances)} registros de {cls.__name__} (skip={skip}, limit={limit})')

            if as_dict:
                return [inst.model_dump() for inst in instances]

            return list(instances)
        except Exception as e:
            logger.error(f'Error al obtener todos los {cls.__name__}: {e}')
            raise

    @classmethod
    async def filter(
        cls: Type[T],
        session: AsyncSession,
        *args: Any,
        skip: int = 0,
        limit: Optional[int] = 100,
        as_dict: bool = False,
        **kwargs: Any
    ) -> List[Union[T, Dict[str, Any]]]:
        """
        Obtiene una lista de instancias que cumplen ciertos criterios de filtro,
        con paginación opcional.

        Permite filtrar por argumentos posicionales (expresiones SQLAlchemy)
        o por argumentos de palabra clave (igualdad simple).

        Ejemplos:
            await Hero.filter(session, name="Spider-Man")
            await Hero.filter(session, Hero.age > 30)
            await Hero.filter(session, Hero.name.like("Super%"), limit=10)

        Args:
            session (AsyncSession): La sesión de base de datos activa.
            *args (Any): Condiciones de filtro como expresiones SQLAlchemy (opcional).
            skip (int): Número de registros a omitir.
            limit (Optional[int]): Número máximo de registros a devolver. Si es None, todos.
            **kwargs (Any): Condiciones de filtro por igualdad de campos (opcional).

        Returns:
            List[T]: Lista de instancias que cumplen los filtros.
        """
        try:
            statement = select(cls)

            # Aplicar filtros de argumentos posicionales (*args)
            if args:
                statement = statement.where(*args)

            # Aplicar filtros de palabra clave (**kwargs) usando filter_by
            # filter_by es conveniente para igualdad simple
            if kwargs:
                statement = statement.filter_by(**kwargs)

            # Aplicar paginación
            statement = statement.offset(skip)
            if limit is not None:
                statement = statement.limit(limit)

            result = await session.execute(statement)
            instances = result.scalars().all()
            filter_desc = f"args={args}, kwargs={kwargs}" if args or kwargs else "sin filtro"
            logger.info(f"Filtrados {len(instances)} registros de {cls.__name__} ({filter_desc}, skip={skip}, limit={limit}).")

            if as_dict:
                return [inst.model_dump() for inst in instances]

            return list(instances)
        except Exception as e:
            logger.error(f'Error al filtrar {cls.__name__}: {e}')
            raise


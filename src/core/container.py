"""
Dependency Injection Container.

Provides a simple DI container for managing service lifetimes
and resolving dependencies throughout the application.
"""

from __future__ import annotations

from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")


class Container:
    """
    Dependency Injection Container.

    Supports singleton and transient service lifetimes.

    Usage:
        # Register a singleton service
        container.register_singleton(ConfigService)

        # Register with interface
        container.register_singleton(ILogger, FileLogger)

        # Register existing instance
        container.register_instance(ConfigService, my_config)

        # Resolve a service
        config = container.resolve(ConfigService)
    """

    _instance: Container | None = None

    def __new__(cls) -> Container:
        """Ensure singleton instance of the container itself."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._services: dict[Type, dict[str, Any]] = {}
            cls._instance._factories: dict[Type, Callable[[], Any]] = {}
        return cls._instance

    def register_singleton(
        self,
        interface: Type[T],
        implementation: Type[T] | None = None
    ) -> None:
        """
        Register a singleton service.

        The same instance will be returned for all resolve calls.

        Args:
            interface: The type/interface to register
            implementation: Optional implementation class (defaults to interface)
        """
        impl = implementation or interface
        self._services[interface] = {
            "implementation": impl,
            "lifetime": "singleton",
            "instance": None,
        }

    def register_transient(
        self,
        interface: Type[T],
        implementation: Type[T] | None = None
    ) -> None:
        """
        Register a transient service.

        A new instance will be created for each resolve call.

        Args:
            interface: The type/interface to register
            implementation: Optional implementation class (defaults to interface)
        """
        impl = implementation or interface
        self._services[interface] = {
            "implementation": impl,
            "lifetime": "transient",
            "instance": None,
        }

    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Register an existing instance.

        The provided instance will be returned for all resolve calls.

        Args:
            interface: The type/interface to register
            instance: The instance to register
        """
        self._services[interface] = {
            "implementation": type(instance),
            "lifetime": "singleton",
            "instance": instance,
        }

    def register_factory(
        self,
        interface: Type[T],
        factory: Callable[[], T]
    ) -> None:
        """
        Register a factory function for creating instances.

        The factory will be called each time the service is resolved.

        Args:
            interface: The type/interface to register
            factory: Factory function that creates instances
        """
        self._factories[interface] = factory
        self._services[interface] = {
            "implementation": None,
            "lifetime": "factory",
            "instance": None,
        }

    def resolve(self, interface: Type[T]) -> T:
        """
        Resolve a service by its interface.

        Args:
            interface: The type/interface to resolve

        Returns:
            The service instance

        Raises:
            KeyError: If the service is not registered
        """
        if interface not in self._services:
            raise KeyError(f"Service {interface.__name__} not registered")

        service_info = self._services[interface]
        lifetime = service_info["lifetime"]

        if lifetime == "factory":
            return self._factories[interface]()

        if lifetime == "singleton":
            if service_info["instance"] is None:
                service_info["instance"] = self._create_instance(
                    service_info["implementation"]
                )
            return service_info["instance"]

        # Transient - always create new instance
        return self._create_instance(service_info["implementation"])

    def _create_instance(self, implementation: Type[T]) -> T:
        """
        Create an instance of a service, resolving constructor dependencies.

        Args:
            implementation: The class to instantiate

        Returns:
            New instance of the implementation
        """
        # For now, simple instantiation without automatic DI
        # Can be extended to support constructor injection
        return implementation()

    def is_registered(self, interface: Type) -> bool:
        """
        Check if a service is registered.

        Args:
            interface: The type/interface to check

        Returns:
            True if registered, False otherwise
        """
        return interface in self._services

    def clear(self) -> None:
        """
        Clear all registered services.

        Useful for testing or application reset.
        """
        self._services.clear()
        self._factories.clear()

    def get_all_registered(self) -> list[Type]:
        """
        Get list of all registered service types.

        Returns:
            List of registered types
        """
        return list(self._services.keys())


# Global container instance
container = Container()

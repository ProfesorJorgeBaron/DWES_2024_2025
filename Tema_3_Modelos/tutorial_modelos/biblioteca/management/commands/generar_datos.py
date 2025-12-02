from django.core.management.base import BaseCommand
from faker import Faker
from biblioteca.models import * 
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generando datos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()

        bibliotecas = []
        for _ in range(10):
            b = Biblioteca.objects.create(
                nombre=fake.company(),
                direccion=fake.address()
            )
            bibliotecas.append(b)

        # 2. Crear 10 Autores
        autores = []
        for _ in range(10):
            a = Autor.objects.create(
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                edad=random.randint(25, 80)
            )
            autores.append(a)

        # 3. Crear 10 Libros
        idiomas = ["ES", "EN", "FR", "IT"]
        libros = []
        for _ in range(10):
            l = Libro.objects.create(
                nombre=fake.sentence(nb_words=4),
                tipo=random.choice(idiomas),
                descripcion=fake.text(max_nb_chars=200),
                fecha_publicacion=fake.date_between(start_date='-10y', end_date='today'),
                biblioteca=random.choice(bibliotecas)
            )
            # Añadir autores 
            l.autores.set(random.sample(autores, random.randint(1, 3)))
            libros.append(l)

        # 4. Crear 10 Clientes
        clientes = []
        for _ in range(10):
            preferido = random.choice(libros)
            c = Cliente.objects.create(
                nombre=fake.name(),
                email=fake.unique.email(),
                puntos=random.uniform(0, 10),
                libros_preferidos=preferido
            )
            clientes.append(c)

        # 5. Crear DatosCliente
        for c in clientes:
            DatosCliente.objects.create(
                cliente=c,
                direccion=fake.address(),
                gustos=fake.text(max_nb_chars=100),
                telefono=fake.random_int(min=600000000, max=699999999)
            )

        # 6. Crear Prestamos
        for c in clientes:
            libros_a_prestar = random.sample(libros, random.randint(1, 3))
            for l in libros_a_prestar:
                Prestamo.objects.create(
                    cliente=c,
                    libro=l,
                    fecha_prestamo=fake.date_time_between(start_date='-1y', end_date='now')
                )

        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))
from django import forms
from .models import *
from datetime import date
import datetime
from .helper import helper
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusquedaLibroForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BusquedaAvanzadaLibroForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)

    textoCategoria = forms.CharField(required=False)    
        
    IDIOMAS = [
        ("ES", "Español"),
        ("EN", "Inglés"),
        ("FR", "Francés"),
        ("IT", "Italiano"),
    ]
  
    idiomas = forms.MultipleChoiceField(choices=IDIOMAS,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                               )
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2025))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Desde",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(1990,2025))
                                  )
    
class LibroForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Libro",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    descripcion = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea())
    
    fecha_publicacion = forms.DateField(label="Fecha Publicación",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget(years=range(1990,2025))
                                        )
    
    IDIOMAS = [
        ("ES", "Español"),
        ("EN", "Inglés"),
        ("FR", "Francés"),
        ("IT", "Italiano"),
    ]
    idioma = forms.ChoiceField(choices=IDIOMAS,
                               initial="ES")
    
    imagen = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        
        super(LibroForm, self).__init__(*args, **kwargs)
        
        bibliotecasDisponibles = helper.obtener_bibliotecas_select()
        self.fields["biblioteca"] = forms.ChoiceField(
            choices=bibliotecasDisponibles,
            widget=forms.Select,
            required=True,
        )
        
        autoresDisponibles = helper.obtener_autores_select()
        self.fields["autores"] = forms.MultipleChoiceField(
            choices= autoresDisponibles,
            required=True,
            help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
        )
        
        categoriasDisponibles = helper.obtener_categorias_select()
        self.fields["categorias"] = forms.MultipleChoiceField(
            choices= categoriasDisponibles,
            required=True,
            help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
        )
        
class LibroActualizarNombreForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Libro",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    

class RegistroForm(UserCreationForm): 
    roles = (
                                (2, 'cliente'),
                                (3, 'bibliotecario'),
            )   
    rol = forms.ChoiceField(choices=roles)  
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','rol')
        
class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
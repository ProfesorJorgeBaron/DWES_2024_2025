from django import forms
from django.forms import ModelForm
from .models import *
from datetime import date
import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput

class LibroForm(forms.Form):
    #Definimos un campo de tipo Texto para el nombre
    nombre = forms.CharField(label="Nombre del Libro",
                             required=True, 
                             max_length=200,
                             help_text="200 caracteres como máximo")
    
    #Definimos un campo de Tipo Textarea para la descripcion
    descripcion = forms.CharField(label="Descripcion",
                                  required=False,
                                  widget=forms.Textarea())
    
    #Definimos un campo de Tipo Fecha para la fecha de publicación
    fecha_publicacion = forms.DateField(label="Fecha Publicación",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget()
                                        )
    
    #Definimos un campo Select para seleccionar el Idioma
    idioma = forms.ChoiceField(choices=Libro.IDIOMAS,
                               initial="ES")
    
    #Definimos un campo Select para seleccionar una biblioteca que es una relacion ManyToOne
    bibliotecasDisponibles = Biblioteca.objects.all()
    biblioteca = forms.ModelChoiceField(
            queryset=bibliotecasDisponibles,
            widget=forms.Select,
            required=True,
            empty_label="Ninguna"
    )
    
     #Definimos un campo Select Múltiple para seleccionar autores en una relación ManyToMany
    autoresDisponibles = Autor.objects.all()
    autores = forms.ModelMultipleChoiceField(
        queryset= autoresDisponibles,
        required=True,
        help_text="Mantén pulsada la tecla control para seleccionar varios elementos"
    )
    
     
    def clean(self):
 
        super().clean()
        
        #Primero obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_publicacion = self.cleaned_data.get('fecha_publicacion')
        idioma = self.cleaned_data.get('idioma')
        biblioteca = self.cleaned_data.get('biblioteca')
        autores = self.cleaned_data.get('autores')
 
        #Comprobamos que no exista un libro con ese nombre
        libroNombre = Libro.objects.get(nombre=nombre)
        if(not libroNombre is None):
             self.add_error('nombre','Ya existe un libro con ese nombre')

        #Comprobamos que el campo descripción no tenga menos de 10 caracteres        
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 3 caracteres')
        
        #Comprobamos que la fecha de publicación sea menor que hoy
        fechaHoy = date.today().strftime("%d-%m-%Y")
        if fechaHoy < fecha_publicacion :
             self.add_error('fecha_publicacion','La fecha de publicacion debe ser menor a Hoy')
        
        #Comprobamos que el idioma no pueda ser en Francés si se ha seleccionado la Biblioteca de la Universidad de Sevilla
        if idioma == "FR" & biblioteca.id == 3:
             self.add_error('idioma','No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
             self.add_error('biblioteca','No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
 
        #Que al menos seleccione dos autores
        if len(autores) < 2:
             self.add_error('autores','Debe seleccionar al menos dos autores')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class LibroModelForm(ModelForm):   
    class Meta:
        model = Libro
        fields = ['nombre','descripcion','fecha_publicacion','idioma','biblioteca','autores']
        labels = {
            "nombre": ("Nombre del Libro"),
        }
        help_texts = {
            "nombre": ("200 caracteres como máximo"),
            "autores":("Mantén pulsada la tecla control para seleccionar varios elementos")
        }
        widgets = {
            "fecha_publicacion":forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        localized_fields = ["fecha_publicacion"]
    
    
    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        fecha_publicacion = self.cleaned_data.get('fecha_publicacion')
        idioma = self.cleaned_data.get('idioma')
        biblioteca = self.cleaned_data.get('biblioteca')
        autores = self.cleaned_data.get('autores')
 
        #Comprobamos que no exista un libro con ese nombre
        libroNombre = Libro.objects.filter(nombre=nombre).first()
        if(not libroNombre is None
           ):
             if(not self.instance is None and libroNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe un libro con ese nombre')

        #Comprobamos que el campo descripción no tenga menos de 10 caracteres        
        if len(descripcion) < 10:
            self.add_error('descripcion','Al menos debes indicar 10 caracteres')
        
        #Comprobamos que la fecha de publicación sea mayor que hoy
        fechaHoy = date.today()
        if fechaHoy > fecha_publicacion :
             self.add_error('fecha_publicacion','La fecha de publicacion debe ser mayor a Hoy')
        
        #Comprobamos que el idioma no pueda ser en Francés si se ha seleccionado la Biblioteca de la Universidad de Sevilla
        if idioma == "FR" and biblioteca.id == 4:
             self.add_error('idioma','No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
             self.add_error('biblioteca','No puede usar la Biblioteca de la Universidad de Sevilla y el idioma Fránces')
 
        #Que al menos seleccione dos autores
        if len(autores) < 2:
             self.add_error('autores','Debe seleccionar al menos dos autores')
        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class BusquedaLibroForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    

class BusquedaAvanzadaLibroForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    
  
    idiomas = forms.MultipleChoiceField(choices=Libro.IDIOMAS,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                               )
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= DatePickerInput()
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Desde",
                                  required=False,
                                  widget= forms.DateInput(format="%Y-%m-%d", 
                                                          attrs={"type": "date"},
                                                          )
                                  )
    
    
    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        idiomas = self.cleaned_data.get('idiomas')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
           
        #Controlamos los campos
        #Ningún campo es obligatorio, pero al menos debe introducir un valor en alguno para buscar
        if(textoBusqueda == "" 
           and len(idiomas) == 0
           and fecha_desde is None
           and fecha_hasta is None
           ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('idiomas','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta','Debe introducir al menos un valor en un campo del formulario')
        else:
            #Si introduce un texto al menos que tenga  3 caracteres o más
            if(textoBusqueda != "" and len(textoBusqueda) < 3):
                self.add_error('textoBusqueda','Debe introducir al menos 3 caracteres')
            
            #La fecha hasta debe ser mayor o igual a fecha desde. Pero sólo se valida si han introducido ambas fechas
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
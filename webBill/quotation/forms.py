from django import forms
import pandas as pd
import microbill as mb
from unidecode import unidecode

class Servicios(object):
    def __init__(self):
        self.equipos = None
        self.equipos_raw = mb.constants.EQUIPOS

        self.descripciones = None
        for equipo in self.equipos_raw:
            setattr(self, equipo, getattr(mb.constants, equipo))
        self.generarCampos()

    def generarCampos(self):
        self.descripciones = {}
        self.equipos = []
        for equipo_s in self.equipos_raw:
            equipo = getattr(self, equipo_s)
            equipo_s = equipo_s.split("_")[0]
            equipo_s = ''.join([c for c in equipo_s if c.isalpha()])
            self.equipos.append(equipo_s)
            self.descripciones[equipo_s] = list(equipo['Descripción'])

    def getField(self, equipo, item):
        fields = []
        for field in (equipo, item):
            field = unidecode(field)
            field = ''.join([c for c in field if (c.isalpha() or c == ' ')])
            field = field.replace(' ', '_')
            fields.append(field)
        return "_".join(fields).lower()

    def getEquipos(self):
        return self.equipos

    def getDescripcionesEquipo(self, equipo):
        return self.descripciones[equipo]

    def getDescripcion(self, equipo, pos):
        return self.descripciones[equipo][pos]

    def __repr__(self):
        txt = []
        for equipo in self.equipos:
            txt.append("\t\t\t%s:\n" % equipo + "\n".join(self.descripciones[equipo]))
        return "\n".join(txt)

class QuoteForm(forms.Form):
    FIELDS = ['nombre', 'institucion', 'documento', 'telefono', 'direccion', 'ciudad', 'correo', 'muestra', 'pago']
    nombre = forms.CharField(label = 'Nombre')
    institucion = forms.CharField(label = 'Institución')
    documento = forms.CharField(label = 'NIT/CC:')
    telefono = forms.CharField(label = 'Teléfono')
    direccion = forms.CharField(label = 'Dirección')
    ciudad = forms.CharField(label = 'Ciudad')
    correo = forms.EmailField(label = 'Correo')
    muestra = forms.CharField(label = 'Muestra')

    TIPO_CHOICES = (("Transferencia interna", "Transferencia interna"),
                    ("Recibo", "Recibo"),
                    ("Factura", "Factura"))

    pago = forms.ChoiceField(label = 'Forma de pago',
            choices = TIPO_CHOICES)

    def __init__(self, *args):
        super(QuoteForm, self).__init__(*args)
        self.servicios = Servicios()
        for equipo in self.servicios.getEquipos():
            for servicio in self.servicios.getDescripcionesEquipo(equipo):
                name = self.servicios.getField(equipo, servicio)
                setattr(self, name, forms.IntegerField(required = False))
                self.fields[name] = getattr(self, name)

    def getEquipo(self):
        for equipo in self.servicios.getEquipos():
            yield equipo

    def getDescripcion(self):
        for equipo in self.servicios.getEquipos():
            for descripcion in self.servicios.getDescripcionesEquipo(equipo):
                yield descripcion

    def getCampo(self):
        for equipo in self.servicios.getEquipos():
            for descripcion in self.servicios.getDescripcionesEquipo(equipo):
                yield getattr(self, self.servicios.getField(equipo, descripcion))
                # yield self.fields[self.servicios.getField(equipo, descripcion)]

    def getEquipoServiciosFields(self):
        temp = []
        for equipo in self.servicios.getEquipos():
            desc = self.servicios.getDescripcionesEquipo(equipo)
            # fields = [self.fields[self.servicios.getField(equipo, d)] for d in desc]
            yield equipo, zip(desc, fields)
            # temp.append([equipo, zip(desc, fields)])
        # return temp

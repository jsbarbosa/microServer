from django import forms
import pandas as pd
import microbill as mb

class Servicios(object):
    def __init__(self):
        self.equipos = None
        self.equipos_raw = mb.constants.EQUIPOS

        self.descripciones = None
        self.equipos_descripciones = None
        for equipo in self.equipos_raw:
            setattr(self, equipo, getattr(mb.constants, equipo))
        self.generarCampos()

    def generarCampos(self):
        self.descripciones = {}
        self.equipos = []
        for equipo_s in self.equipos_raw:
            equipo = getattr(self, equipo_s)
            equipo_s = equipo_s.split("_")[0]
            self.equipos.append(equipo_s)
            self.descripciones[equipo_s] = list(equipo['Descripción'])
        self.equipos_descripciones = [(equipo, self.descripciones[equipo]) for equipo in self.equipos]

    def getField(self, equipo, item):
        equipo = equipo.replace(' ', '_')
        item = item.replace(' ', '_')
        return "%s_%s" % (equipo, item)

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

    def __init__(self):
        super(QuoteForm, self).__init__()
        self.servicios = Servicios()
        for equipo in self.servicios.getEquipos():
            for servicio in self.servicios.getDescripcionesEquipo(equipo):
                self.fields[self.servicios.getField(equipo, servicio)] = forms.IntegerField()

    def serviciosHTML(self):
        text = []
        for (i, equipo) in enumerate(self.servicios.getEquipos()):
            fields = []
            txt = """
<div class="container">
  <div class="panel-group">
    <div class="panel panel-default">
      <div class="panel-heading">
        <button class="panel-title">
          <a data-toggle="collapse" href="#collapse%d">%s</a>
        </button>
      </div>
      <div id="collapse%d" class="panel-collapse collapse">
        <div class="container">
            %s
        </div>
      </div>
    </div>
  </div>
</div>
    """
            for servicio in self.servicios.getDescripcionesEquipo(equipo):
                field = self.servicios.getField(equipo, servicio)
                label = r'<label for = "id_%s" class = "col-form-label"> "%s" <\label>' % (field, servicio)
                widget = r'<div class>\n<inputt type = "number" class="numberinput numberInput form-control" required id = "id_%s"<\div>' % (field)
                fields.append(label + "\n" + widget)
            txt = txt % (i, equipo, i, "\n".join(fields))
            text.append(txt)
        return "\n".join(text)

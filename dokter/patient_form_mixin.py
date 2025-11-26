from .patient_create_form import CreatePatientMixin
from .patient_edit_form import EditPatientMixin
from .patient_konsul_form import KonsulPatientMixin


class PatientFormMixin(CreatePatientMixin, EditPatientMixin, KonsulPatientMixin):
    """
    Mixin gabungan:
    - CreatePatientMixin  (tambah pasien)
    - EditPatientMixin    (edit pasien)
    - KonsulPatientMixin  (atur tanggal konsultasi)
    """

    pass

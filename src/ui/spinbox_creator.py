from PyQt5.QtWidgets import QWidget, QVBoxLayout

def create_spinbox(object, min_value, max_value, single_step, parent_checkbox, default_value=None):
    spinbox = object
    spinbox.setMinimum(min_value)
    spinbox.setMaximum(max_value)
    spinbox.setSingleStep(single_step)
    spinbox.setEnabled(parent_checkbox.isChecked())

    def on_checkbox_state_changed(state):
        spinbox.setEnabled(state == 2)

    parent_checkbox.stateChanged.connect(on_checkbox_state_changed)

    if default_value is not None:
        spinbox.setValue(default_value)

    layout = QVBoxLayout()
    layout.addWidget(spinbox)

    widget = QWidget()
    widget.setLayout(layout)
    return widget
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from control.config_manager import config, config_manager
from control.label_manager import LabelManager


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_gui = parent
        uic.loadUi("labelCloud/ressources/settings_interface.ui", self)
        self.fill_with_current_settings()

        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.chancel)
        self.reset_button.clicked.connect(self.reset)

    def fill_with_current_settings(self):
        # File
        self.lineEdit_pointcloudfolder.setText(config.get("FILE", "pointcloud_folder"))
        self.lineEdit_labelfolder.setText(config.get("FILE", "label_folder"))

        # Pointcloud
        self.doubleSpinBox_pointsize.setValue(config.getfloat("POINTCLOUD", "POINT_SIZE"))
        self.lineEdit_pointcolor.setText(config["POINTCLOUD"]["colorless_color"])
        self.checkBox_colorizecolorless.setChecked(config.getboolean("POINTCLOUD", "colorless_colorize"))
        self.doubleSpinBox_standardtranslation.setValue(config.getfloat("POINTCLOUD", "std_translation"))
        self.doubleSpinBox_standardzoom.setValue(config.getfloat("POINTCLOUD", "std_zoom"))

        # Label
        self.comboBox_labelformat.addItems(LabelManager.LABEL_FORMATS)  # TODO: Fix visualization
        self.comboBox_labelformat.setCurrentText(config.get("LABEL", "label_format"))
        self.plainTextEdit_objectclasses.setPlainText(config.get("LABEL", "object_classes"))
        self.lineEdit_standardobjectclass.setText(config.get("LABEL", "std_object_class"))
        self.spinBox_exportprecision.setValue(config.getint("LABEL", "export_precision"))
        self.doubleSpinBox_minbboxdimensions.setValue(config.getfloat("LABEL", "min_boundingbox_dimension"))
        self.doubleSpinBox_stdbboxlength.setValue(config.getfloat("LABEL", "std_boundingbox_length"))
        self.doubleSpinBox_stdbboxwidth.setValue(config.getfloat("LABEL", "std_boundingbox_width"))
        self.doubleSpinBox_stdbboxheight.setValue(config.getfloat("LABEL", "std_boundingbox_height"))
        self.doubleSpinBox_stdbboxtranslation.setValue(config.getfloat("LABEL", "std_translation"))
        self.doubleSpinBox_stdbboxrotation.setValue(config.getfloat("LABEL", "std_rotation"))
        self.doubleSpinBox_stdbboxscaling.setValue(config.getfloat("LABEL", "std_scaling"))

        # User Interface
        self.checkBox_zrotationonly.setChecked(config.getboolean("USER_INTERFACE", "z_rotation_only"))
        self.checkBox_showfloor.setChecked(config.getboolean("USER_INTERFACE", "show_floor"))
        self.checkBox_showbboxorientation.setChecked(config.getboolean("USER_INTERFACE", "show_orientation"))
        self.spinBox_viewingprecision.setValue(config.getint("USER_INTERFACE", "viewing_precision"))
        self.lineEdit_backgroundcolor.setText(config.get("USER_INTERFACE", "background_color"))

    def save(self) -> None:
        # File
        config["FILE"]["pointcloud_folder"] = self.lineEdit_pointcloudfolder.text()
        config["FILE"]["label_folder"] = self.lineEdit_labelfolder.text()

        # Pointcloud
        config["POINTCLOUD"]["point_size"] = str(self.doubleSpinBox_pointsize.value())
        config["POINTCLOUD"]["colorless_color"] = self.lineEdit_pointcolor.text()
        config["POINTCLOUD"]["colorless_colorize"] = str(self.checkBox_colorizecolorless.isChecked())
        config["POINTCLOUD"]["std_translation"] = str(self.doubleSpinBox_standardtranslation.value())
        config["POINTCLOUD"]["std_zoom"] = str(self.doubleSpinBox_standardzoom.value())

        # Label
        config["LABEL"]["label_format"] = self.comboBox_labelformat.currentText()
        config["LABEL"]["object_classes"] = self.plainTextEdit_objectclasses.toPlainText()
        config["LABEL"]["std_object_class"] = self.lineEdit_standardobjectclass.text()
        config["LABEL"]["export_precision"] = str(self.spinBox_exportprecision.value())
        config["LABEL"]["min_boundingbox_dimension"] = str(self.doubleSpinBox_minbboxdimensions.value())
        config["LABEL"]["std_boundingbox_length"] = str(self.doubleSpinBox_stdbboxlength.value())
        config["LABEL"]["std_boundingbox_width"] = str(self.doubleSpinBox_stdbboxwidth.value())
        config["LABEL"]["std_boundingbox_height"] = str(self.doubleSpinBox_stdbboxheight.value())
        config["LABEL"]["std_translation"] = str(self.doubleSpinBox_stdbboxtranslation.value())
        config["LABEL"]["std_rotation"] = str(self.doubleSpinBox_stdbboxrotation.value())
        config["LABEL"]["std_scaling"] = str(self.doubleSpinBox_stdbboxscaling.value())

        # User Interface
        config["USER_INTERFACE"]["z_rotation_only"] = str(self.checkBox_zrotationonly.isChecked())
        config["USER_INTERFACE"]["show_floor"] = str(self.checkBox_showfloor.isChecked())
        config["USER_INTERFACE"]["show_orientation"] = str(self.checkBox_showbboxorientation.isChecked())
        config["USER_INTERFACE"]["background_color"] = self.lineEdit_backgroundcolor.text()
        config["USER_INTERFACE"]["viewing_precision"] = str(self.spinBox_viewingprecision.value())

        config_manager.write_into_file()
        self.parent_gui.set_checkbox_states()
        print("Saved and activated new configuration!")

    def reset(self):
        config_manager.reset_to_default()
        self.fill_with_current_settings()

    def chancel(self) -> None:
        print("Settings dialog was chanceled!")

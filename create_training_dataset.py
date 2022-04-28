import os
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QButtonGroup
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

import deeplabcut
from deeplabcut.utils import auxiliaryfunctions

from components import (
    DefaultTab,
    ShuffleSpinBox,
    TrainingSetSpinBox,
    _create_grid_layout,
    _create_horizontal_layout,
    _create_label_widget,
)
from dlc_params import DLC_Params


class CreateTrainingDataset(DefaultTab):
    def __init__(self, root, parent, h1_description):
        super(CreateTrainingDataset, self).__init__(root, parent, h1_description)

        self.method = "automatic"
        self.userfeedback = False
        self.model_comparison = False

        self.main_layout.addWidget(_create_label_widget("Attributes", "font:bold"))
        self.layout_attributes = _create_grid_layout(margins=(20, 0, 0, 0))
        self._generate_layout_attributes(self.layout_attributes)
        self.main_layout.addLayout(self.layout_attributes)

        self.ok_button = QtWidgets.QPushButton("Ok")
        self.ok_button.setMinimumWidth(150)
        self.ok_button.clicked.connect(self.create_training_dataset)

        self.main_layout.addWidget(self.ok_button, alignment=Qt.AlignRight)

    def _generate_layout_attributes(self, layout):
        # Shuffle
        shuffle_label = QtWidgets.QLabel("Shuffle")
        self.shuffle = ShuffleSpinBox(root=self.root, parent=self)

        # Trainingset index
        trainingset_label = QtWidgets.QLabel("Trainingset index")
        self.trainingset = TrainingSetSpinBox(root=self.root, parent=self)

        # Augmentation method
        augmentation_label = QtWidgets.QLabel("Augmentation method")
        self.aug_choice = QComboBox()
        self.aug_choice.setMinimumWidth(150)
        self.aug_choice.addItems(DLC_Params.IMAGE_AUGMENTERS)
        self.aug_choice.setCurrentText("imgaug")
        self.aug_choice.currentTextChanged.connect(self.log_augmentation_choice)

        # Neural Network
        nnet_label = QtWidgets.QLabel("Network architecture")
        self.net_choice = QComboBox()
        self.net_choice.setMinimumWidth(150)
        self.net_choice.addItems(DLC_Params.NNETS)
        self.net_choice.setCurrentText("resnet_50")
        self.net_choice.currentTextChanged.connect(self.log_net_choice)

        layout.addWidget(nnet_label, 0, 0)
        layout.addWidget(self.net_choice, 0, 1)
        layout.addWidget(augmentation_label, 1, 0)
        layout.addWidget(self.aug_choice, 1, 1)
        layout.addWidget(shuffle_label, 0, 2)
        layout.addWidget(self.shuffle, 0, 3)
        layout.addWidget(trainingset_label, 1, 2)
        layout.addWidget(self.trainingset, 1, 3)

    def log_net_choice(self, net):
        self.root.logger.info(f"Network architecture set to {net.upper()}")

    def log_augmentation_choice(self, augmentation):
        self.root.logger.info(f"Image augmentation set to {augmentation.upper()}")

    def create_training_dataset(self):
        num_shuffles = self.shuffle.value()
        config_file = auxiliaryfunctions.read_config(self.config)
        trainindex = self.trainingindex.value()

        userfeedback = self.userfeedback

        if config_file.get("multianimalproject", False):
            print("multianimalproject")
            deeplabcut.create_multianimaltraining_dataset(
                self.config,
                num_shuffles,
                Shuffles=[self.shuffle.value()],
                net_type=self.net_choice.currentText(),
            )
        else:
            if self.model_comparison == False:
                deeplabcut.create_training_dataset(
                    self.config,
                    num_shuffles,
                    Shuffles=[self.shuffle.value()],
                    userfeedback=userfeedback,
                    net_type=self.net_choice.currentText(),
                    augmenter_type=self.aug_choice.currentText(),
                )
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("The training dataset is successfully created.")
                msg.setInformativeText(
                    "Use the function 'train_network' to start training. Happy training!"
                )

                msg.setWindowTitle("Info")
                msg.setMinimumWidth(900)
                self.logo_dir = (
                    os.path.dirname(os.path.realpath("logo.png")) + os.path.sep
                )
                self.logo = self.logo_dir + "/assets/logo.png"
                msg.setWindowIcon(QIcon(self.logo))
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()

            else:
                # comparison = True
                # TODO: finish model_comparison
                deeplabcut.create_training_model_comparison(
                    self.config,
                    trainindex=trainindex,
                    num_shuffles=num_shuffles,
                    userfeedback=userfeedback,
                    net_types=self.net_type,
                    augmenter_types=self.aug_type,
                )

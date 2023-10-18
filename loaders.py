from coremltools import ComputeUnit

import folder_paths
from comfy import supported_models_base, model_management
from comfy.latent_formats import SD15
from comfy.model_patcher import ModelPatcher
from .logger import logger
from .model import CoreMLModelWrapper


class CoreMLLoader:
    PACKAGE_DIRNAME = ""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "coreml_name": (list(s.coreml_filenames().keys()),),
                "compute_unit": (list(ComputeUnit.__members__.keys()),)
            }
        }

    RETURN_TYPES = ("COREML_MODEL",)
    FUNCTION = "load"
    CATEGORY = "CoreML Suite"

    @classmethod
    def coreml_filenames(cls):
        return {
            p.split('/')[-1]:
                p for p in
            folder_paths.get_filename_list_(cls.PACKAGE_DIRNAME)[1]
            if p.endswith((".mlpackage", ".mlmodelc"))
        }

    def load(self, coreml_name, compute_unit):
        logger.info(f"Loading {coreml_name}")

        coreml_path = self.coreml_filenames()[coreml_name]

        sources = "compiled" if coreml_name.endswith(
            ".mlmodelc") else "packages"

        # TODO: This is a dummy model config, but it should be enough to
        #  get the model to load - implement a proper model config
        model_config = supported_models_base.BASE({})
        model_config.latent_format = SD15()
        model_config.unet_config = {"disable_unet_model_creation": True}
        return (CoreMLModelWrapper(model_config, coreml_path, compute_unit,
                                   sources),)


class CoreMLLoaderCkpt(CoreMLLoader):
    PACKAGE_DIRNAME = "checkpoints"
    RETURN_TYPES = ("MODEL", "CLIP", "VAE")

    def load(self, coreml_name, compute_unit):
        # TODO: Implement this
        pass


class CoreMLLoaderTextEncoder(CoreMLLoader):
    PACKAGE_DIRNAME = "clip"
    RETURN_TYPES = ("CLIP",)

    def load(self, coreml_name, compute_unit):
        # TODO: Implement this
        pass


class CoreMLLoaderUNet(CoreMLLoader):
    PACKAGE_DIRNAME = "unet"
    RETURN_TYPES = ("MODEL",)

    def load(self, coreml_name, compute_unit):
        coreml_model = super().load(coreml_name, compute_unit)[0]

        return (
            ModelPatcher(coreml_model, model_management.get_torch_device(),
                         None),)


class CoreMLLoaderVAE(CoreMLLoader):
    PACKAGE_DIRNAME = "vae"
    RETURN_TYPES = ("VAE",)

    def load(self, coreml_name, compute_unit):
        # TODO: Implement this
        pass

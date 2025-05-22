from typing import Any, Optional, Union

from invokeai.app.invocations.controlnet import ControlField, ControlNetInvocation
from invokeai.app.invocations.fields import FluxConditioningField
from invokeai.app.invocations.flux_controlnet import FluxControlNetField, FluxControlNetInvocation
from invokeai.app.invocations.flux_redux import FluxReduxConditioningField, FluxReduxInvocation
from invokeai.app.invocations.flux_text_encoder import FluxTextEncoderInvocation
from invokeai.app.invocations.ip_adapter import IPAdapterField, IPAdapterInvocation
from invokeai.app.invocations.t2i_adapter import T2IAdapterField, T2IAdapterInvocation
from invokeai.invocation_api import (
    BaseInvocationOutput,
    FieldDescriptions,
    Input,
    InputField,
    InvocationContext,
    OutputField,
    invocation,
    invocation_output,
)


def append_list(item_cls: type[Any], new_item: Any, items: Union[Any, list[Any], None] = None) -> list[Any]:
    """Combines any number of items or lists into a single list,
    ensuring consistency in type.

    Args:
        item_cls: The expected type of elements in the list.
        new_item: Additional item to append.
        items: An existing list or single item of type `item_cls`.

    Returns:
        The updated list containing valid items.

    Raises:
        ValueError: If any item in the list or new_item is not of the expected type.
    """

    if not isinstance(new_item, item_cls):
        raise ValueError(f"Invalid new_item type in: {new_item},  expected {item_cls}")

    if items is None:
        return [new_item]

    result: list[item_cls] = []

    if isinstance(items, item_cls):
        result.append(items)
    elif isinstance(items, list) and all(isinstance(i, item_cls) for i in items):
        result.extend(items)
    else:
        raise ValueError(f"Invalid items type in: {items},  expected {item_cls}")

    result.append(new_item)
    return result


@invocation_output("control_list_output")
class ControlListOutput(BaseInvocationOutput):
    control_list: list[ControlField] = OutputField(description=FieldDescriptions.control, title="ControlNet List")


@invocation(
    "controlnet-linked",
    title="ControlNet-Linked",
    tags=["controlnet"],
    category="controlnet",
    version="1.1.2",
)
class ControlNetLinkedInvocation(ControlNetInvocation):
    """Collects ControlNet info to pass to other nodes."""

    control_list: Optional[Union[ControlField, list[ControlField]]] = InputField(
        description=FieldDescriptions.control,
        default=None,
        title="ControlNet-List",
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> ControlListOutput:
        output = super().invoke(context).control
        control_list = append_list(ControlField, output, self.control_list)
        return ControlListOutput(control_list=control_list)


@invocation_output("ip_adapter_list_output")
class IPAdapterListOutput(BaseInvocationOutput):
    ip_adapter_list: list[IPAdapterField] = OutputField(
        description=FieldDescriptions.ip_adapter, title="IP-Adapter List"
    )


@invocation(
    "ip_adapter_linked",
    title="IP-Adapter-Linked",
    tags=["ip_adapter", "control"],
    category="ip_adapter",
    version="1.1.2",
)
class IPAdapterLinkedInvocation(IPAdapterInvocation):
    """Collects IP-Adapter info to pass to other nodes."""

    ip_adapter_list: Optional[Union[IPAdapterField, list[IPAdapterField]]] = InputField(
        description=FieldDescriptions.ip_adapter,
        title="IP-Adapter List",
        default=None,
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> IPAdapterListOutput:
        output = super().invoke(context).ip_adapter
        ip_adapter_list = append_list(IPAdapterField, output, self.ip_adapter_list)
        return IPAdapterListOutput(ip_adapter_list=ip_adapter_list)


@invocation_output("t2i_adapter_list_output")
class T2IAdapterListOutput(BaseInvocationOutput):
    t2i_adapter_list: list[T2IAdapterField] = OutputField(
        description=FieldDescriptions.t2i_adapter, title="T2I Adapter List"
    )


@invocation(
    "t2i_adapter_linked",
    title="T2I-Adapter-Linked",
    tags=["t2i_adapter", "control"],
    category="t2i_adapter",
    version="1.0.2",
)
class T2IAdapterLinkedInvocation(T2IAdapterInvocation):
    """Collects T2I-Adapter info to pass to other nodes."""

    t2i_adapter_list: Optional[Union[T2IAdapterField, list[T2IAdapterField]]] = InputField(
        description=FieldDescriptions.t2i_adapter,
        title="T2I Adapter List",
        default=None,
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> T2IAdapterListOutput:
        output = super().invoke(context).t2i_adapter
        t2i_adapter_list = append_list(T2IAdapterField, output, self.t2i_adapter_list)
        return T2IAdapterListOutput(t2i_adapter_list=t2i_adapter_list)


@invocation_output("flux_redux_list_output")
class FluxReduxListOutput(BaseInvocationOutput):
    redux_conditioning_list: list[FluxReduxConditioningField] = OutputField(
        description=FieldDescriptions.flux_redux_conditioning, title="FLUX Redux Conditioning List"
    )


@invocation(
    "flux_redux_linked",
    title="FLUX Redux-Linked",
    tags=["flux", "redux", "control"],
    category="ip_adapter",
    version="1.0.0",
)
class FluxReduxLinkedInvocation(FluxReduxInvocation):
    """Collects FLUX Redux conditioning info to pass to other nodes."""

    redux_conditioning_list: Optional[Union[FluxReduxConditioningField, list[FluxReduxConditioningField]]] = InputField(
        description="FLUX Redux conditioning list",
        title="FLUX Redux Conditioning List",
        default=None,
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> FluxReduxListOutput:
        output = super().invoke(context).redux_cond
        redux_conditioning_list = append_list(FluxReduxConditioningField, output, self.redux_conditioning_list)
        return FluxReduxListOutput(redux_conditioning_list=redux_conditioning_list)


@invocation_output("flux_controlnet_list_output")
class FluxControlNetListOutput(BaseInvocationOutput):
    controlnet_list: list[FluxControlNetField] = OutputField(
        description=FieldDescriptions.control, title="FLUX ControlNet List"
    )


@invocation(
    "flux_controlnet_linked",
    title="FLUX ControlNet-Linked",
    tags=["flux", "controlnet"],
    category="controlnet",
    version="1.0.0",
)
class FluxControlNetLinkedInvocation(FluxControlNetInvocation):
    """Collects FLUX ControlNet info to pass to other nodes."""

    controlnet_list: Optional[Union[FluxControlNetField, list[FluxControlNetField]]] = InputField(
        description="FLUX ControlNet List",
        default=None,
        title="FLUX ControlNet List",
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> FluxControlNetListOutput:
        output = super().invoke(context).control
        controlnet_list = append_list(FluxControlNetField, output, self.controlnet_list)
        return FluxControlNetListOutput(controlnet_list=controlnet_list)


@invocation_output("flux_text_encoder_list_output")
class FluxTextEncoderListOutput(BaseInvocationOutput):
    """Output for a list of FLUX text encoder conditioning."""

    flux_text_encoder_list: list[FluxConditioningField] = OutputField(
        description=FieldDescriptions.cond, title="FLUX Text Encoder Conditioning List"
    )


@invocation(
    "flux_text_encoder_linked",
    title="Prompt - FLUX Linked",
    tags=["flux", "text_encoder", "conditioning"],
    category="conditioning",
    version="1.0.0",
)
class FluxTextEncoderLinkedInvocation(FluxTextEncoderInvocation):
    """Collects FLUX prompt conditionings to pass to other nodes."""

    flux_text_encoder_list: Optional[Union[FluxConditioningField, list[FluxConditioningField]]] = InputField(
        description=FieldDescriptions.cond,
        title="FLUX Text Encoder Conditioning List",
        default=None,
        input=Input.Connection,
        ui_order=0,
    )

    def invoke(self, context: InvocationContext) -> FluxTextEncoderListOutput:
        output_conditioning = super().invoke(context).conditioning
        flux_text_encoder_list = append_list(FluxConditioningField, output_conditioning, self.flux_text_encoder_list)
        return FluxTextEncoderListOutput(flux_text_encoder_list=flux_text_encoder_list)

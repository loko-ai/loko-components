from typing import List

from loko_extensions.utils.pathutils import find_path
import json


class Input:
    """
        A component's input. Components can have multiple inputs.

        Example:

            >>> input1 = Input(id="input1", label="input1", to="output")
            >>> input2 = Input(id="input2", label="input2", to="output")
            >>> comp1 = Component(name="comp1", inputs=[input1, input2])
            >>> save_extensions([comp1])

        Args:
            id (str): The name of the input point.
            label (str): The visualized name. By default, it is set to the id value.
            service (str): Represents the path to the linked service. Default: `""`
            to (str): The name of the connected output.
        """
    def __init__(self, id, label=None, service=None, to="output"):

        self.id = id
        self.label = label or id
        self.service = service or ""
        self.to = to


class Output:
    """
        A component's output. Components can have multiple outputs.

        Example:

            >>> output1 = Output(id="output1", label="output1")
            >>> output2 = Output(id="output", label="output2")
            >>> comp1 = Component(name="comp1", outputs=[output1, output2])
            >>> save_extensions([comp1])

        Args:
            id (str): The name of the output point.
            label (str): The visualized name. By default, it is set to the id value.
        """
    def __init__(self, id, label=None):
        self.id = id
        self.label = label or id


class Arg:
    """
            A component's argument. Arguments are used to configure the block's parameters. See also: `Select`,
                `Dynamic`.

            Example:

                >>> model_name = Arg(name="model_name", type="text", label="Model Name", helper="Helper text")
                >>> train = Arg(name="train", type="boolean", label="Train Model", description="Helper text")
                >>> comp1 = Component(name="comp1", args=[model_name, train])
                >>> save_extensions([comp1])

            Args:
                name (str): The name of the parameter.
                type (str): The parameter's type. Available types are: "text", "boolean", "number", "path", "files".
                    Default: `"text"`
                label (str): The visualized name. By default, it is set to the name value.
                helper (str): The explanation of the parameter usage.
                description (str): The explanation of the parameter usage. In this case it'll be displayed by clicking
                    on the "i" icon.
                group (str): The name of the parameter's section. It's used to divide parameters into groups.
                value: The default value of the parameter.
            """
    def __init__(self, name, type="text", label=None, helper="", description="", group="", value=None):
        self.name = name
        self.type = type
        self.label = label or name
        self.helper = helper
        self.group = group
        self.value = value
        self.description = description


class Select(Arg):
    """
            A component's argument. Select is used to show a list of available options to configure the block's
                parameter. See also: `Arg`, `Dynamic`.

            Example:

                >>> task = Select(name="task", label="Task", options=["sentiment analysis", "text generation",
                    "question answering"])
                >>> comp1 = Component(name="comp1", args=[task])
                >>> save_extensions([comp1])

            Args:
                name (str): The name of the parameter.
                options (list): The list of available parameter's options.
                label (str): The visualized name. By default, it is set to the name value.
                helper (str): The explanation of the parameter usage.
                description (str): The explanation of the parameter usage. In this case it'll be displayed by clicking
                    on the "i" icon.
                group (str): The name of the parameter's section. It's used to divide parameters into groups.
                value: The default value of the parameter.
                """
    def __init__(self, name, options, label=None, helper="", description="", group="", value=None):
        super().__init__(name, "select", label, helper, description, group, value)
        self.options = options

class Dynamic(Arg):
    """
            A component's argument. Dynamic is used to dynamically show a parameter's configuration.
                See also: `Arg`, `Select`.

            Example:
                >>> task = Select(name="task", label="Task", group="Task Settings", options=["sentiment analysis", "text generation", "question answering"])
                >>> max_length = Dynamic(name="max_length", label="Max Length", dynamicType="number", parent="task", group="Task Settings", value=30, condition="{parent}===\\"text generation\\"")
                >>> comp1 = Component(name='comp1', args=[task, max_length])
                >>> save_extensions([comp1])

            Args:
                name (str): The name of the parameter.
                parent (str): The name of the parameter it depends on.
                condition (str): The parameter will be displayed only when this condition is verified. The programming
                    language used in this case is JavaScript.
                label (str): The visualized name. By default, it is set to the name value.
                dynamicType (str): The parameter's type. Available types are: "text", "boolean", "number", "path",
                    "files". Default: `"text"`
                helper (str): The explanation of the parameter usage.
                description (str): The explanation of the parameter usage. In this case it'll be displayed by clicking
                    on the "i" icon.
                group (str): The name of the parameter's section. It's used to divide parameters into groups.
                value: The default value of the parameter.
                """
    def __init__(self, name, parent, condition, label=None, dynamicType="text", helper="", description="",
                 group="", value=None):
        super().__init__(name, "dynamic", label, helper, description, group, value)
        self.parent = parent
        self.condition = condition
        self.dynamicType = dynamicType

class Component:
    """
        A customized Loko component.

        Example:
            >>> comp1 = Component(name="comp1")
            >>> save_extensions([comp1])

        Args:
            name (str): The name of the component.
            description (str): The explanation of the component.
            inputs (List[Input]): The list of the component's inputs. Default: `[Input("input")]`
            outputs (List[Output]): The list of the component's outputs. Default: `[Output("output")]`
            args (List[Arg]): The list of the component's arguments. Default: `None`
            configured (bool): Set to `False` if configurations are required. Default: `True`
        """
    def __init__(self, name, description="", inputs=None, outputs=None,args=None, configured=True):
        self.name = name
        self.description = description
        self.inputs = inputs or [Input("input")]
        self.outputs = outputs or [Output("output")]
        self.args = args or []
        self.configured = configured

    def to_dict(self):
        values = {x.name: x.value for x in self.args if x.value}
        options = dict(group="Custom", icon="RiTyphoonFill", click=None, values=values,
                       args=[x.__dict__ for x in self.args])
        return dict(name=self.name, description=self.description, configured=self.configured,
                    inputs=[x.__dict__ for x in self.inputs],
                    outputs=[x.__dict__ for x in self.outputs], options=options)


def save_extensions(comps, path="extensions"):
    """
        Save a list of components into the components.json file.
    """
    output_path = find_path(path)
    output = output_path / "components.json"
    with output.open("w") as o:
        json.dump([comp.to_dict() for comp in comps], o, indent=1)

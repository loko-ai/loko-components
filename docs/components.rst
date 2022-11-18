Components
==========

Get started with Components
---------------------------

Components in LOKO AI are saved into:

.. code-block:: console

    Home/loko/projects/<yourprojectname>/extensions/components.json

You can create a new script into your project.

For example:

.. code-block:: console

    Home/loko/projects/<yourprojectname>/business/create_components.py

.. code-block:: python

    from loko_extensions.model.components import Arg, Component, save_extensions

    ### args ###
    model_name = Arg(name="model_name", type="text", label="Model Name", helper="Helper text")
    train = Arg(name="train", type="boolean", label="Train Model", description="Helper text")

    ### component ###
    comp1 = Component(name="My First Component", args=[model_name, train], group="Custom")

    ### save ###
    save_extensions([comp1])

When you run the script, it'll update your file ``components.json``.

If you open your project using Loko, you'll find in the `Custom` section of the sidebar your first component:
``My First Component``.
You can drag and drop the component into your project and double click on it.

.. image:: https://raw.githubusercontent.com/loko-ai/doc_resources/main/loko_extensions/imgs/loko.png
  :width: 700
  :align: center

|

You just created your first :py:meth:`~loko_extensions.model.components.Component` in Loko.

The ``description`` of the component is visualized in the **Doc** section. Here you can add details of the component's
usage.

Parameter ``group`` is used to set the name of the section the component belongs to, by default you can find it in the
`Custom` section.

``trigger`` is True if the component doesn't necessarily need an input (input and outputs are shown in the next
section). To work properly it needs a single input named "input".

In order to visualize that your component requires configurations, you have to set ``configured`` to False.

You can customize the ``icon`` choosing one from here:
`react-icons/ri <https://react-icons.github.io/react-icons/icons?name=ri>`_.


Inputs/Outputs
----------------

Components' inputs are linked to your services. Let's create a new service into:

.. code-block:: console

    Home/loko/projects/<yourprojectname>/services/services.py

If you want to change your services path, remember also to change it into your ``Dockerfile``.

For example:

.. code-block:: python

    @bp.post('/myfirstservice')
    @doc.consumes(doc.JsonBody({}), location="body")
    @extract_value_args()
    async def f(value, args):
        return sanic.json(dict(msg="Hello world!"))

You can now add :py:meth:`~loko_extensions.model.components.Input` and
:py:meth:`~loko_extensions.model.components.Output` to your first component:

.. code-block:: python

    from loko_extensions.model.components import Arg, Component, save_extensions, Input, Output

    ### args ###
    model_name = Arg(name="model_name", type="text", label="Model Name", helper="Helper text")
    train = Arg(name="train", type="boolean", label="Train Model", description="Helper text")

    ### inputs/outputs ###
    input1 = Input(id='input', label='Input', service='myfirstservice', to='output')
    output1 = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="My First Component", args=[model_name, train],
                      inputs=[input1], outputs=[output1])

    ### save ###
    save_extensions([comp1])

``label`` represents the visualized name in Loko. By default, it is set to the id value.
``to`` represents the link between input and output.

- Note that in ``service`` the first ``/`` is skipped.

Arguments
---------

We saw in the first example a *text* and a *boolean* :py:meth:`~loko_extensions.model.components.Arg`.
Available types are: “text”, “boolean”, “number”, “path”, “files”, “directories”, “code”, “password”, “email”, “area”.

You can add arguments' explanation using ``description`` or ``helper``.
In the first case you'll find the information symbol, in the second one the description will be explicitly written near
to the argument name.

``group`` is used to group arguments into different tabs.

Let's see an example:

.. code-block:: python

    from loko_extensions.model.components import Arg, Component, save_extensions, Input, Output

    ### args ###
    model_name = Arg(name="model_name", type="text",
                     label="Model Name", helper="Helper text", required=True)
    partial = Arg(name="partial", type="boolean", label="Partial Fit",
                  group='Fit Parameters', value=False)
    metrics = Arg(name="metrics", type="boolean", label="Compute Metrics",
                  group='Fit Parameters', value=True)
    proba = Arg(name="proba", type="boolean", label="Predict Proba",
                group='Predict Parameters', value=True)

    ### inputs/outputs ###
    fit_input = Input(id='fit', label='Fit', service='fitservice', to='fit')
    fit_output = Output(id='fit', label='Fit')

    predict_input = Input(id='predict', label='Predict', service='predictservice', to='predict')
    predict_output = Output(id='predict', label='Predict')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[model_name, partial, metrics, proba],
                      inputs=[fit_input, predict_input],
                      outputs=[fit_output, predict_output],
                      configured=False)

    ### save ###
    save_extensions([comp1])

In this case we'll have two different tabs: *Fit Parameters* and *Predict Parameters*.

You can use ``value`` to set default value for the argument and set ``required`` to True if the parameter is required.

.. image:: https://raw.githubusercontent.com/loko-ai/doc_resources/main/loko_extensions/imgs/loko2.png
  :width: 700
  :align: center

|

Select
^^^^^^^

:py:meth:`~loko_extensions.model.components.Select` arguments allow to set all the values that an argument can assume,
using ``options``.

Example:

.. code-block:: python

    from loko_extensions.model.components import Component, save_extensions, Input, Output, \
                                                Select

    ### args ###
    task = Select(name="task", label="Task", options=["sentiment analysis",
                  "text generation", "question answering"])

    ### inputs/outputs ###

    predict_input = Input(id='input', label='Input', service='mlservice', to='output')
    predict_output = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[task],
                      inputs=[predict_input],
                      outputs=[predict_output])

    ### save ###
    save_extensions([comp1])

.. image:: https://raw.githubusercontent.com/loko-ai/doc_resources/main/loko_extensions/imgs/loko3.png
  :width: 700
  :align: center

|

AsyncSelect
^^^^^^^^^^^^

:py:meth:`~loko_extensions.model.components.AsyncSelect` argument is used to show a list of available options to
configure the block’s parameter. Unlike Select argument, it takes options from the result of a GET request.

Example:

.. code-block:: python

    from loko_extensions.model.components import Component, save_extensions, Input, Output, \
                                            AsyncSelect

    ### args ###
    task = AsyncSelect(name='task', label='Task',
                       url='http://localhost:9999/routes/first_project/tasks')

    ### inputs/outputs ###

    predict_input = Input(id='input', label='Input', service='mlservice', to='output')
    predict_output = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[task],
                      inputs=[predict_input],
                      outputs=[predict_output])

    ### save ###
    save_extensions([comp1])

In this case the list of options is the result of ``http://localhost:9999/routes/first_project/tasks``.


MultiKeyValue
^^^^^^^^^^^^^^

:py:meth:`~loko_extensions.model.components.MultiKeyValue` argument is used to set lists of variable length.

For example, Selector component's *keys* argument is a MultiKeyValue. Here you can set one or more keys to be selected
from the input dictionary: *Name*, *Sex*, *Age*.

.. image:: https://user-images.githubusercontent.com/30443495/201632579-97b590bf-c22c-45ec-bb3b-5010049c3faf.png
  :width: 700
  :align: center

|

We can also set more than one :py:meth:`~loko_extensions.model.components.MKVField`. You first have to list all the
MKVFields and then add them to the MultiKeyValue.

Example:

.. code-block:: python

    from loko_extensions.model.components import Component, save_extensions, Input, Output, \
                                                MKVField, MultiKeyValue

    ### args ###

    mkvfields = [MKVField(name='name', label='Name'),
                 MKVField(name='type', label='Type')]
    expl_vars = MultiKeyValue(name='expl_vars', label='Explanatory Variables', fields=mkvfields)

    ### inputs/outputs ###

    predict_input = Input(id='input', label='Input', service='mlservice', to='output')
    predict_output = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[expl_vars],
                      inputs=[predict_input],
                      outputs=[predict_output])

    ### save ###
    save_extensions([comp1])



Dynamic
^^^^^^^

:py:meth:`~loko_extensions.model.components.Dynamic` arguments are used to dynamically show a parameter’s
configuration. Available dynamic types are: “text”, “boolean”, “number”, “path”, “files”, “directories”, “code”,
“password”, “email”, “area”, “select”, “asyncSelect”, “multiKeyValue”.

Example:

.. code-block:: python

    from loko_extensions.model.components import Component, save_extensions, Input, Output, \
                                                Select, Dynamic

    ### args ###

    task = Select(name="task", label="Task", group="Task Settings",
                  options=["sentiment analysis", "text generation", "question answering"])
    max_length = Dynamic(name="max_length", label="Max Length", dynamicType="number",
                         parent="task", group="Task Settings", value=30,
                         condition="{parent}===\"text generation\"")

    ### inputs/outputs ###

    predict_input = Input(id='input', label='Input', service='mlservice', to='output')
    predict_output = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[task, max_length],
                      inputs=[predict_input],
                      outputs=[predict_output])

    ### save ###
    save_extensions([comp1])

*Max Length* is a specific parameter used by the text generation task.
It is a number field (i.e. ``"dynamicType"="number"``), depends on Task value (i.e. ``"parent"="task"``)
and it'll be displayed only when Task is set to text generation (i.e. ``"condition"="{parent}===\"text generation\""``).

Events
------

:py:meth:`~loko_extensions.model.components.Events` are used to visualize the status of the component. You can emit
messages using the gateway socket and visualize them on the top of your block.

Example:

.. code-block:: python

    from loko_extensions.model.components import Component, save_extensions, Input, Output, \
                                                Events, Arg

    ### args ###

    show_msg = Arg(name='show_msg', label='Show msg', type='boolean', value=True)

    ### inputs/outputs ###

    predict_input = Input(id='input', label='Input', service='mlservice', to='output')
    predict_output = Output(id='output', label='Output')

    ### component ###
    comp1 = Component(name="ML Component",
                      args=[show_msg],
                      inputs=[predict_input],
                      outputs=[predict_output],
                      events=Events(type="ml_msg", field="show_msg"))

    ### save ###
    save_extensions([comp1])

You have to choose an identifier of the messages, named ``type``, and define an argument whose
value allows the visualization of the emitted messages.
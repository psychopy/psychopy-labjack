from psychopy.experiment.components import BaseComponent, Param
from psychopy.localization import _translate
from pathlib import Path


class LabjackComponent(BaseComponent):
    categories = ["I/O", "EEG"]
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'parallel.png'
    iconSVG = Path(__file__).parent / 'LabjackComponent.svg'
    tooltip = _translate('Send signals to a Labjack')
    
    def __init__(
            self, 
            exp, 
            parentName, 
            name="labjack",
            startType="time (s)", 
            startVal="",
            stopType="duration (s)", 
            stopVal="stopVal",
            startEstim="", 
            durationEstim="",
            startData=1,
            stopData=0,
            register="EIO",
            syncScreen=True
    ):
        BaseComponent.__init__(
            self, 
            exp, 
            parentName, 
            name,
            startType=startType, 
            startVal=startVal,
            stopType=stopType, 
            stopVal=stopVal,
            startEstim=startEstim, 
            durationEstim=durationEstim
        )

        self.type = 'Labjack'
        self.exp.requireImport(
            importName='labjacks',
            importFrom='psychopy_labjack'
        )

        # params
        self.order += [
            "register",
            "startData", 
            "stopData",
        ]

        self.params['startData'] = Param(
            startData, 
            categ="Basic",
            valType="code", 
            inputType="single",
            label=_translate("Start data"),
            hint=_translate(
                "Data to be sent at 'start'"
            )
        )

        self.params['stopData'] = Param(
            stopData, 
            categ="Basic",
            valType='code', 
            inputType="single", 
            label=_translate("Stop data"),
            hint=_translate(
                "Data to be sent at 'end'"
            )
        )

        self.params['register'] = Param(
            register,
            valType="str",
            inputType="choice",
            allowedVals=["EIO", "FIO"],
            label=_translate("U3 register"),
            hint=_translate(
                "U3 Register to write byte to"
            )
        )

        self.params['syncScreen'] = Param(
            syncScreen, 
            categ="Data",
            valType='bool', 
            inputType="bool", 
            allowedVals=[True, False],
            label=_translate("Sync to screen"),
            hint=_translate(
                "If the parallel port data relates to visual stimuli then sync its pulse to the " 
                "screen refresh"
            )
        )

    def writeInitCode(self, buff):
        # create
        code = (
            "# initialize %(name)s\n"
            "%(name)s = labjacks.U3()\n"
        )
        buff.writeIndentedLines(code % self.params)

    def writeFrameCode(self, buff):
        # when Component starts...
        indented = self.writeStartTestCode(buff)
        if indented:
            # set start data
            code = (
                "# set %(name)s start data\n"
            )
            if not self.params['syncScreen'].val:
                code += (
                    "%(name)s.setData(\n"
                    "    int(%(startData)s), \n"
                    "    address=%(register)s\n"
                    ")\n"
                )
            else:
                code += (
                    "win.callOnFlip(\n"
                    "    %(name)s.setData,\n"
                    "    int(%(startData)s),\n"
                    "    address=%(register)s\n"
                    ")\n"
                )
            buff.writeIndentedLines(code % self.params)
        # dedent
        buff.setIndentLevel(-indented, relative=True)

        # when Component stops...
        indented = self.writeStartTestCode(buff)
        if indented:
            # set stop data
            code = (
                "# set %(name)s stop data\n"
            )
            if not self.params['syncScreen'].val:
                code += (
                    "%(name)s.setData(\n"
                    "    int(%(stopData)s), \n"
                    "    address=%(register)s\n"
                    ")\n"
                )
            else:
                code += (
                    "win.callOnFlip(\n"
                    "    %(name)s.setData,\n"
                    "    int(%(stopData)s),\n"
                    "    address=%(register)s\n"
                    ")\n"
                )
            buff.writeIndentedLines(code % self.params)
        # dedent
        buff.setIndentLevel(-indented, relative=True)

    def writeRoutineEndCode(self, buff):
        # write normal end code
        BaseComponent.writeRoutineEndCode(self, buff=buff)
        # set stop data on stop in case the Component finished before the Routine
        code = (
            "# set %(name)s stop data\n"
        )
        if not self.params['syncScreen'].val:
            code += (
                "%(name)s.setData(\n"
                "    int(%(stopData)s), \n"
                "    address=%(register)s\n"
                ")\n"
            )
        else:
            code += (
                "win.callOnFlip(\n"
                "    %(name)s.setData,\n"
                "    int(%(stopData)s),\n"
                "    address=%(register)s\n"
                ")\n"
            )
        buff.writeIndentedLines(code % self.params)

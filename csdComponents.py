# -*- coding: UTF-8 -*-


options = """
<CsoundSynthesizer>

<CsOptions>
; Audio/midi flags here according to platform
 -o ../audio/capricho.wav -W ;;; file output options (name and format)
</CsOptions>

<CsInstruments>
"""

endOrcStartSco = """
</CsInstruments>

<CsScore>
"""

functionTables = """
f1 0 16384 10 1
"""

durationFunction = """
; Dummy function to extend performance duration (allows held notes to
;end as intended).
;f0	59

"""

endFile = """
e
</CsScore>
</CsoundSynthesizer>
"""

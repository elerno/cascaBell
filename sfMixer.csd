<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform
; Audio out   Audio in    No messages
-odac           -iadc     -+rtaudio=alsa -d     ;;;RT audio I/O
; For Non-realtime ouput leave only the line below:
; -o FLslidBnk.wav -W ;;; for file output any platform
</CsOptions>
<CsInstruments>

sr = 44100
kr = 441
ksmps = 100
nchnls = 1
0dbfs	= 1

giScaleAmp = .5

iTableSize = 64 ; must be a power of 2  
giOutTable ftgen 0, 0, iTableSize, -23, "mixLevelsLoad.txt"

FLpanel "Soundfile loops mixer", 600, 380, 50, 50
    ;Number of sliders
    iNum = 16
    ; Width of the slider bank in piXels
    iWidth = 350
    ; Height of the slider in piXels
    iHeight = 260
    ; Distance of the left edge of the slider
    ; from the left edge of the panel
    iX = 30
    ; Distance of the top edge of the slider 
    ; from the top edge of the panel
    iY = 10
    ; Button type
    iTypeTable = -23
    ; Table containing fader types
    iExpTable  = 0 ; linear faders 
    FLslidBnk " ", iNum , giOutTable , iWidth , iHeight , iX, iY, \
    iTypeTable, iExpTable, 1
    ; Save button
    iOn = 1
    iOff = 23
    iXb = 400
    iYb = 10
    gkButton, ihb1 FLbutton "Save fader values", iOn, iOff, 21, 200, 40, iXb, iYb, -1
    ; Mute button
    iOn1 = 0
    iOff1 = 1
    iXb1 = 400
    iYb1 = 60
    gkMute, ihb2 FLbutton "Mute", iOn1, iOff1, 23, 200, 40, iXb1, iYb1, -1
    
; End of panel contents
FLpanelEnd
; Run the widget thread!
FLrun


strset 1, "../stones/violin1/samples/1vln1.wav"
strset 2, "../stones/violin1/samples/2vln1.wav"
strset 3, "../stones/violin1/samples/3vln1.wav"
strset 4, "../stones/violin1/samples/4vln1.wav"
strset 5, "../stones/violin1/samples/5vln1.wav"
strset 6, "../stones/violin1/samples/6vln1.wav"
strset 7, "../stones/violin1/samples/7vln1.wav"
strset 8, "../stones/violin1/samples/8vln1.wav"
strset 9, "../stones/violin1/samples/9vln1.wav"
strset 10, "../stones/violin1/samples/10vln1.wav"
strset 11, "../stones/violin1/samples/11vln1.wav"
strset 12, "../stones/violin1/samples/13vln1.wav"
strset 13, "../stones/violin1/samples/14vln1.wav"
strset 14, "../stones/violin1/samples/15vln1.wav"
strset 15, "../stones/violin1/samples/16vln1.wav"

	instr 1
iFileNum	= p4

iPitch		= 1
iSkipTime 	= 0
iWrap		= 1

aLoop diskin2 iFileNum, iPitch, iSkipTime, iWrap

kAmpScale table iFileNum, giOutTable

printf "Channel%d - AmpScale = %f\n", kAmpScale, iFileNum, kAmpScale
out aLoop * kAmpScale * giScaleAmp * gkMute
	endin


	instr 2
if gkButton != 23 then
	ftsavek "mixLevelsSave.txt", gkButton, 1, giOutTable
	gkButton = 23
endif
	endin

</CsInstruments>
<CsScore>

; Instrument 1 will play a note for 1 hour.
i1 0 3600 1
i1 0 3600 2
i1 0 3600 3
i1 0 3600 4
i1 0 3600 5
i1 0 3600 6
i1 0 3600 7
i1 0 3600 8
i1 0 3600 9
i1 0 3600 10
i1 0 3600 11
i1 0 3600 12
i1 0 3600 13
i1 0 3600 14
i1 0 3600 15
i2 0 3600
e

</CsScore>
</CsoundSynthesizer>

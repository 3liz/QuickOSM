# Makefile for QuickOSM

i18n_1_prepare:
	@echo Updating strings locally 1/4
	@./update_strings.sh fr de en es es_ES fi it nl pt pt_BR ru zh_TW

i18n_2_push:
	@echo Push strings to Transifex 2/4
	@tx push -s

i18n_3_pull:
	@echo Pull strings from Transifex 3/4
	@tx pull -a

i18n_4_compile:
	@echo Compile TS files to QM 4/4
	@lrelease i18n/QuickOSM_fr.ts -qm i18n/QuickOSM_fr.qm
	@lrelease i18n/QuickOSM_de.ts -qm i18n/QuickOSM_de.qm
	@lrelease i18n/QuickOSM_es.ts -qm i18n/QuickOSM_es.qm
	@lrelease i18n/QuickOSM_es_ES.ts -qm i18n/QuickOSM_es_ES.qm
	@lrelease i18n/QuickOSM_fi.ts -qm i18n/QuickOSM_fi.qm
	@lrelease i18n/QuickOSM_it.ts -qm i18n/QuickOSM_it.qm
	@lrelease i18n/QuickOSM_nl.ts -qm i18n/QuickOSM_nl.qm
	@lrelease i18n/QuickOSM_de.ts -qm i18n/QuickOSM_pt.qm
	@lrelease i18n/QuickOSM_pt_BR.ts -qm i18n/QuickOSM_pt_BR.qm
	@lrelease i18n/QuickOSM_ru.ts -qm i18n/QuickOSM_ru.qm
	@lrelease i18n/QuickOSM_zh-TW.ts -qm i18n/QuickOSM_zh-TW.qm

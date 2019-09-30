# Makefile for QuickOSM

i18n_1_prepare:
	@echo Updating strings locally 1/4
	@./update_strings.sh fr de en es es_ES fi id it nl pt pt_BR ru zh_TW

i18n_2_push:
	@echo Push strings to Transifex 2/4
	@tx push -s

i18n_3_pull:
	@echo Pull strings from Transifex 3/4
	@tx pull -a

i18n_4_compile:
	@echo Compile TS files to QM 4/4
	@lrelease resources/i18n/QuickOSM_fr.ts -qm resources/i18n/QuickOSM_fr.qm
	@lrelease resources/i18n/QuickOSM_de.ts -qm resources/i18n/QuickOSM_de.qm
	@lrelease resources/i18n/QuickOSM_es.ts -qm resources/i18n/QuickOSM_es.qm
	@lrelease resources/i18n/QuickOSM_es_ES.ts -qm resources/i18n/QuickOSM_es_ES.qm
	@lrelease resources/i18n/QuickOSM_fi.ts -qm resources/i18n/QuickOSM_fi.qm
	@lrelease resources/i18n/QuickOSM_id.ts -qm resources/i18n/QuickOSM_id.qm
	@lrelease resources/i18n/QuickOSM_it.ts -qm resources/i18n/QuickOSM_it.qm
	@lrelease resources/i18n/QuickOSM_nl.ts -qm resources/i18n/QuickOSM_nl.qm
	@lrelease resources/i18n/QuickOSM_de.ts -qm resources/i18n/QuickOSM_pt.qm
	@lrelease resources/i18n/QuickOSM_pt_BR.ts -qm resources/i18n/QuickOSM_pt_BR.qm
	@lrelease resources/i18n/QuickOSM_ru.ts -qm resources/i18n/QuickOSM_ru.qm
	@lrelease resources/i18n/QuickOSM_zh_TW.ts -qm resources/i18n/QuickOSM_zh_TW.qm

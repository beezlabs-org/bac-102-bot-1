import random
from dataclasses import dataclass
from tulipService import Bot
from tulipService.model.variableModel import VariableModel


@dataclass
class BotInputSchema:
    companycode: VariableModel = None
    companyCodeSampleCount: VariableModel = None
    manualEntitiesCompanyCode: VariableModel = None


@dataclass
class BotOutputSchema:
    def __init__(self):
        self.manualEntitiesCompanyCodeList = VariableModel()
        self.nonManualEntitiesCompanyCodeList = VariableModel()
        self.manualFlag = VariableModel()
        self.nonManualFlag = VariableModel()


class BotLogic(Bot):
    def __init__(self) -> None:
        super().__init__()
        try:
            self.outputs = BotOutputSchema()
            self.input = self.bot_input.get_proposedBotInputs(BotInputs=BotInputSchema)

            self.company_codes = self.input.companycode.value
            self.company_code_sample_count = int(self.input.companyCodeSampleCount.value)
            self.manual_entities_company_code = self.input.manualEntitiesCompanyCode.value

        except Exception as error:
            self.log.error(f"Error initializing BotLogic: {error}")

    def main(self):
        """Bot Logic code"""
        try:
            self.log.info("Randomly select a specified number of company codes")
            # Step 1: Randomly select a specified number of company codes
            selected_company_codes = random.sample(self.company_codes, self.company_code_sample_count)

            # Step 2: Validate the selected company codes against the list of manual entity company codes
            self.log.info("Validate the selected company codes against the list of manual entity company codes")
            manual_entities_list = []
            non_manual_entities_list = []

            for code in selected_company_codes:
                if code in self.manual_entities_company_code:
                    manual_entities_list.append(code)
                else:
                    non_manual_entities_list.append(code)
            self.log.info("manual and non-manual entities list created")

            self.outputs.manualEntitiesCompanyCodeList.value = manual_entities_list
            self.outputs.nonManualEntitiesCompanyCodeList.value = non_manual_entities_list

            manual_flag = bool(manual_entities_list)
            non_manual_flag = bool(non_manual_entities_list)
            self.outputs.manualFlag.value = manual_flag
            self.outputs.nonManualFlag.value = non_manual_flag

            self.bot_output.success("SUCCESS")
        except Exception as e:
            self.log.error(f"Error in main execution: {e}")
            self.bot_output.error(e)

        finally:
            self.log.info("Bot execution completed.")

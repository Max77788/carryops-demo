from pathlib import Path
import unittest


HTML = Path(__file__).resolve().parents[1].joinpath("demo", "index.html").read_text()


class ChemicalBidWorkflowTests(unittest.TestCase):
    def test_shipper_can_enter_chemical_load_requirements(self):
        for field in ("postOrigin", "postDest", "postEquip", "postCommodity", "postChemical", "postHazmat", "postPickup", "postDelivery", "postTons", "postLoads", "postModeOpen", "postModeSet", "postRate", "postDeadline"):
            with self.subTest(field=field):
                self.assertTrue(f'id="{field}"' in HTML, field)

    def test_only_active_verified_matching_carriers_are_invitable(self):
        self.assertTrue("function eligibleCarriersForLoad" in HTML)
        eligibility = HTML.split("function eligibleCarriersForLoad", 1)[1].split("\n}", 1)[0]
        for rule in ("c.status==='Active'", "c.verified", "c.equipmentTypes", "criteria.chemical", "c.chemicalCapable", "criteria.hazmat", "c.hazmatEndorsed"):
            with self.subTest(rule=rule):
                self.assertTrue(rule in eligibility, rule)

    def test_form_previews_matching_carriers_and_submission_uses_selected_list(self):
        self.assertTrue('id="eligibleCarrierChoices"' in HTML)
        self.assertTrue("function refreshBidCarrierChoices" in HTML)
        submit = HTML.split("function submitNewLoad()", 1)[1].split("\n}", 1)[0]
        self.assertTrue("input[name=" in submit and "inviteCarrier" in submit, "selected carrier checkboxes are read")
        for contract in ("postMode", "postHazmat", "postChemical", "postDeadline", "eligibleCarriersForLoad", "durationDays", "totalLoads", "onboarded carriers", "handled separately by the admin"):
            with self.subTest(contract=contract):
                self.assertTrue(contract in submit or contract in HTML, contract)

    def test_carrier_bid_uses_load_tonnage_and_accepts_only_valid_invitation(self):
        self.assertTrue("function tonsPerLoad" in HTML)
        bid = HTML.split("function submitBid(loadId)", 1)[1].split("\n}", 1)[0]
        self.assertTrue("perTonPrice(l,amount)" in bid)
        self.assertTrue("l.status!=='Open'" in bid and "l.invited.includes(cid)" in bid)
        self.assertFalse("amount/26" in bid)

    def test_seeded_chemical_bid_scenario_is_explicitly_demo_data(self):
        for evidence in ("Chemical haul", "Industrial solvents", "hazmatEndorsed", "Tanker", "Illustrative demo fixture", "Illustrative demo data"):
            with self.subTest(evidence=evidence):
                self.assertTrue(evidence in HTML, evidence)


if __name__ == "__main__":
    unittest.main()

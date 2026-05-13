from __future__ import annotations

import unittest

from keiji.approval.human_review_packet import build_review_packet


class HumanReviewPacketTest(unittest.TestCase):
    def test_review_packet_always_requires_human_approval(self) -> None:
        packet = build_review_packet(
            target_type="purchase",
            target_id="candidate-1",
            summary="Review purchase candidate",
            reasons=("p3_review",),
        )
        self.assertTrue(packet.requires_human_approval)
        self.assertEqual("purchase", packet.to_dict()["target_type"])


if __name__ == "__main__":
    unittest.main()

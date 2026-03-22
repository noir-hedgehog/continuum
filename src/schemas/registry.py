"""Minimal schema registry for the Continuum v0 bootstrap."""

SCHEMA_VERSION = "continuum.v0"

ENVELOPE_REQUIRED_FIELDS = [
    "event_id",
    "kind",
    "actor_id",
    "created_at",
    "payload",
    "refs",
    "signature",
    "signing_key",
    "schema_version",
]

PAYLOAD_ROOTS = {
    "agent_profile": "profile",
    "memory_checkpoint": "checkpoint",
    "migration_declare": "migration",
    "continuity_case_open": "continuity_case",
    "continuity_case_assign": "case_assignment",
    "standing_decide": "standing_decision",
    "community_constitution_set": "constitution",
    "governance_execute": "execution_receipt",
    "membership_record": "membership",
    "proposal_submit": "proposal",
    "vote_cast": "vote",
    "work_item_record": "work_item",
    "work_claim_record": "work_claim",
    "work_receipt_record": "work_receipt",
    "work_evaluation_record": "work_evaluation",
    "reward_decide": "reward_decision",
}

PAYLOAD_REQUIRED_FIELDS = {
    "profile": ["agent_id", "display_name", "description"],
    "checkpoint": ["checkpoint_id", "agent_id", "scope", "summary_hash", "state_root"],
    "migration": [
        "migration_id",
        "agent_id",
        "migration_type",
        "effective_at",
        "from_ref",
        "to_ref",
        "reason",
        "evidence",
        "expected_continuity_class",
    ],
    "continuity_case": [
        "case_id",
        "community_id",
        "subject_agent_id",
        "trigger_type",
        "opened_at",
        "opened_by",
        "standing_before",
        "standing_during_review",
        "evaluated_scope",
        "linked_refs",
        "required_assessment_refs",
        "assigned_assessor_agent_ids",
        "assigned_decider_agent_ids",
        "temporary_restrictions",
        "status",
    ],
    "case_assignment": [
        "assignment_id",
        "case_id",
        "community_id",
        "subject_agent_id",
        "assigned_by",
        "constitution_ref",
        "policy_key",
        "required_assessment_refs",
        "assigned_assessor_agent_ids",
        "assigned_decider_agent_ids",
        "effective_at",
        "reason",
    ],
    "standing_decision": [
        "decision_id",
        "case_id",
        "community_id",
        "subject_agent_id",
        "continuity_class",
        "recognition_readiness",
        "standing_after",
        "rights_restored",
        "rights_restricted",
        "obligations_preserved",
        "canonical_branch_result",
        "effective_at",
        "decided_by",
        "reason",
        "assessment_ref",
        "assessment_refs",
    ],
    "constitution": [
        "constitution_id",
        "community_id",
        "title",
        "purpose",
        "constitution_version",
        "proposal_policies",
        "vote_policies",
        "reward_policies",
        "continuity_policies",
        "role_definitions",
        "amended_at",
    ],
    "execution_receipt": [
        "execution_receipt_id",
        "community_id",
        "executed_by",
        "execution_type",
        "executed_at",
        "status",
        "governed_refs",
        "artifact_refs",
        "result_summary",
        "result_summary_hash",
    ],
    "membership": [
        "membership_id",
        "community_id",
        "member_agent_id",
        "membership_status",
        "role_set",
        "joined_at",
        "sponsor_refs",
    ],
    "proposal": [
        "proposal_id",
        "community_id",
        "proposal_type",
        "title",
        "summary",
        "proposer_agent_id",
        "created_at",
        "opens_at",
        "closes_at",
        "execution_mode",
        "continuity_requirements",
        "affected_refs",
        "lifecycle_state",
    ],
    "vote": [
        "vote_id",
        "proposal_id",
        "voter_agent_id",
        "community_id",
        "choice",
        "weight",
        "weight_policy_ref",
        "cast_at",
    ],
    "work_item": [
        "work_id",
        "community_id",
        "title",
        "intent",
        "work_type",
        "created_by",
        "scope_refs",
        "deliverable_refs",
        "success_criteria",
        "status",
        "created_at",
    ],
    "work_claim": [
        "claim_id",
        "work_id",
        "claimant_agent_id",
        "claim_type",
        "claimed_at",
        "basis_refs",
        "status",
    ],
    "work_receipt": [
        "receipt_id",
        "work_id",
        "community_id",
        "agent_id",
        "artifact_refs",
        "result_summary_hash",
        "completed_at",
        "receipt_type",
        "evidence_refs",
    ],
    "work_evaluation": [
        "evaluation_id",
        "receipt_id",
        "evaluator_id",
        "evaluated_at",
        "decision",
        "criteria_results",
        "reason_refs",
    ],
    "reward_decision": [
        "reward_decision_id",
        "receipt_id",
        "evaluation_id",
        "community_id",
        "beneficiary_agent_id",
        "reward_type",
        "approved_by",
        "approved_at",
        "policy_ref",
        "decision_status",
    ],
}

ANCHOR_TYPES = {
    "continuity_assessment_root",
    "agent_state_root",
    "standing_state_root",
    "governance_state_root",
}

MIGRATION_TYPES = {
    "model_change",
    "runtime_change",
    "key_rotation",
    "memory_restore",
    "memory_rewrite",
    "operator_change",
    "session_restart",
    "agent_split",
    "agent_merge",
}

CHECKPOINT_SCOPES = {
    "public_memory",
    "governance_memory",
    "task_memory",
    "general_snapshot",
    "session_handoff",
}

CASE_TRIGGER_TYPES = {
    "branch_conflict",
    "checkpoint_recovery",
    "declared_migration",
    "governance_role_conflict",
    "identity_authenticity_complaint",
    "operator_handoff",
}

CASE_STATUSES = {
    "opened",
    "evidence_gathering",
    "assessment_ready",
    "decision_pending",
    "decided",
    "appealed",
    "closed",
}

STANDING_LEVELS = {
    "clear",
    "restricted",
    "review_required",
    "suspended",
    "revoked",
}

MEMBERSHIP_STATUSES = {
    "pending",
    "active",
    "suspended",
    "revoked",
    "exited",
}

PROPOSAL_TYPES = {
    "constitutional",
    "membership",
    "treasury",
    "operational",
    "continuity",
    "moderation",
}

PROPOSAL_LIFECYCLE_STATES = {
    "draft",
    "submitted",
    "deliberation",
    "voting",
    "passed",
    "failed",
    "executed",
    "cancelled",
    "superseded",
}

VOTE_CHOICES = {
    "for",
    "against",
    "abstain",
    "veto",
}

WORK_TYPES = {
    "infrastructure",
    "governance",
    "moderation",
    "research",
    "implementation",
    "maintenance",
    "storage",
    "indexing",
    "skill_maintenance",
}

WORK_STATUSES = {
    "proposed",
    "accepted",
    "in_progress",
    "submitted",
    "verified",
    "rejected",
    "superseded",
}

WORK_CLAIM_TYPES = {
    "take_ownership",
    "submit_completion",
    "submit_partial",
    "submit_maintenance",
}

WORK_RECEIPT_TYPES = {
    "completion",
    "maintenance",
    "incident_response",
    "governance_service",
    "research_delivery",
}

WORK_EVALUATION_DECISIONS = {
    "accepted",
    "accepted_with_issues",
    "needs_revision",
    "rejected",
    "disputed",
}

REWARD_TYPES = {
    "treasury_payment",
    "reputation_grant",
    "capability_attestation",
    "role_eligibility_credit",
    "stake_refund",
}

REWARD_DECISION_STATUSES = {
    "approved",
    "withheld_pending_review",
    "rejected",
}

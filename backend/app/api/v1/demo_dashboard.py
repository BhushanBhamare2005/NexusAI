from fastapi import APIRouter, Depends, HTTPException

from app.core.security import require

router = APIRouter(prefix="/demo", tags=["demo"])
_DEMO_ROLES = {"demo_manager", "demo_senior_agent", "demo_agent"}

_TEAMS = [
    {
        "senior_id": "senior-1",
        "senior_name": "Sofia Chen",
        "agents": [
            {"id": "agent-1", "name": "Maya Patel", "completion_rate": 92},
            {"id": "agent-2", "name": "Liam Brooks", "completion_rate": 88},
            {"id": "agent-3", "name": "Zoe Carter", "completion_rate": 81},
        ],
    },
    {
        "senior_id": "senior-2",
        "senior_name": "Noah Reed",
        "agents": [
            {"id": "agent-4", "name": "Arjun Mehta", "completion_rate": 90},
            {"id": "agent-5", "name": "Elena Torres", "completion_rate": 85},
            {"id": "agent-6", "name": "Theo Kim", "completion_rate": 78},
        ],
    },
]

_TASKS = [
    {
        "id": "DEMO-T101",
        "title": "Reconcile a delayed payment confirmation",
        "assignee_id": "agent-1",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T102",
        "title": "Review a duplicate notification report",
        "assignee_id": "agent-1",
        "status": "In progress",
        "progress": 65,
        "due": "Today",
    },
    {
        "id": "DEMO-T103",
        "title": "Prepare a refund-status case summary",
        "assignee_id": "agent-2",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T104",
        "title": "Verify a sample settlement timeline",
        "assignee_id": "agent-2",
        "status": "Completed",
        "progress": 100,
        "due": "Tomorrow",
    },
    {
        "id": "DEMO-T105",
        "title": "Document a simulated chargeback inquiry",
        "assignee_id": "agent-3",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T106",
        "title": "Complete a sample merchant follow-up",
        "assignee_id": "agent-3",
        "status": "Pending",
        "progress": 0,
        "due": "Tomorrow",
    },
    {
        "id": "DEMO-T107",
        "title": "Review a sample authorization decline",
        "assignee_id": "agent-4",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T108",
        "title": "Summarize a fictional payout delay",
        "assignee_id": "agent-4",
        "status": "In progress",
        "progress": 45,
        "due": "Tomorrow",
    },
    {
        "id": "DEMO-T109",
        "title": "Check a simulated duplicate-payment case",
        "assignee_id": "agent-5",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T110",
        "title": "Draft a sample resolution summary",
        "assignee_id": "agent-5",
        "status": "In progress",
        "progress": 70,
        "due": "Tomorrow",
    },
    {
        "id": "DEMO-T111",
        "title": "Review a fictional refund inquiry",
        "assignee_id": "agent-6",
        "status": "Completed",
        "progress": 100,
        "due": "Today",
    },
    {
        "id": "DEMO-T112",
        "title": "Classify a sample transaction question",
        "assignee_id": "agent-6",
        "status": "Pending",
        "progress": 0,
        "due": "Tomorrow",
    },
]

_ACTIVITIES = [
    {
        "id": "DEMO-A201",
        "actor_id": "agent-1",
        "text": "Maya Patel completed the payment-confirmation review.",
        "when": "Today · 10:15 AM",
    },
    {
        "id": "DEMO-A202",
        "actor_id": "agent-2",
        "text": "Liam Brooks closed the sample refund-status summary.",
        "when": "Today · 9:40 AM",
    },
    {
        "id": "DEMO-A203",
        "actor_id": "agent-3",
        "text": "Zoe Carter escalated a simulated chargeback for review.",
        "when": "Today · 9:05 AM",
    },
    {
        "id": "DEMO-A204",
        "actor_id": "agent-4",
        "text": "Arjun Mehta completed the authorization-decline review.",
        "when": "Today · 8:50 AM",
    },
    {
        "id": "DEMO-A205",
        "actor_id": "agent-5",
        "text": "Elena Torres updated a fictional resolution summary.",
        "when": "Yesterday · 4:30 PM",
    },
    {
        "id": "DEMO-A206",
        "actor_id": "agent-6",
        "text": "Theo Kim added notes to a sample refund inquiry.",
        "when": "Yesterday · 3:55 PM",
    },
    {
        "id": "DEMO-A207",
        "actor_id": "senior-1",
        "text": "Sofia Chen reviewed the team's synthetic case queue.",
        "when": "Today · 10:30 AM",
    },
    {
        "id": "DEMO-A208",
        "actor_id": "senior-2",
        "text": "Noah Reed checked the team's sample workload.",
        "when": "Today · 9:20 AM",
    },
]

_PRODUCTIVITY = [
    {"period": "Mon", "completed": 7, "target": 8},
    {"period": "Tue", "completed": 9, "target": 8},
    {"period": "Wed", "completed": 8, "target": 8},
    {"period": "Thu", "completed": 11, "target": 9},
    {"period": "Fri", "completed": 10, "target": 9},
]

_AGENT_PRODUCTIVITY = [
    {"period": "Mon", "completed": 2, "target": 2},
    {"period": "Tue", "completed": 3, "target": 2},
    {"period": "Wed", "completed": 2, "target": 2},
    {"period": "Thu", "completed": 4, "target": 3},
    {"period": "Fri", "completed": 3, "target": 3},
]


def _status_counts(tasks: list[dict]) -> list[dict[str, int | str]]:
    statuses = ("Completed", "In progress", "Pending")
    return [
        {"status": status, "count": sum(task["status"] == status for task in tasks)}
        for status in statuses
    ]


def _member_payload(team: dict) -> list[dict]:
    members = [
        {
            "name": team["senior_name"],
            "role": "Senior Agent",
            "status": "On track",
            "completion_rate": 94,
        }
    ]
    members.extend(
        {
            "name": agent["name"],
            "role": "Agent",
            "status": "On track" if agent["completion_rate"] >= 85 else "Monitoring",
            "completion_rate": agent["completion_rate"],
        }
        for agent in team["agents"]
    )
    return members


def _task_payload(tasks: list[dict], agent_names: dict[str, str]) -> list[dict]:
    return [
        {
            "id": task["id"],
            "title": task["title"],
            "assignee": agent_names[task["assignee_id"]],
            "status": task["status"],
            "progress": task["progress"],
            "due": task["due"],
        }
        for task in tasks
    ]


def _dashboard(role: str) -> dict:
    agent_by_id = {
        agent["id"]: agent
        for team in _TEAMS
        for agent in team["agents"]
    }

    if role == "demo_manager":
        agent_ids = set(agent_by_id)
        tasks = [task for task in _TASKS if task["assignee_id"] in agent_ids]
        completed = sum(task["status"] == "Completed" for task in tasks)
        return {
            "label": "Synthetic team performance",
            "notice": "All names, tasks, activity, and metrics on this page are fictional demo data.",
            "scope": "team",
            "profile": None,
            "metrics": [
                {"label": "Demo agents", "value": len(agent_by_id)},
                {"label": "Senior agents", "value": len(_TEAMS)},
                {"label": "Tasks completed", "value": completed},
                {
                    "label": "Task completion rate",
                    "value": round(completed / len(tasks) * 100),
                    "unit": "%",
                },
            ],
            "team_members": [
                member
                for team in _TEAMS
                for member in _member_payload(team)
            ],
            "tasks": _task_payload(tasks, {key: value["name"] for key, value in agent_by_id.items()}),
            "task_analytics": _status_counts(tasks),
            "productivity": _PRODUCTIVITY,
            "activities": _ACTIVITIES,
            "reports": [
                {
                    "title": "Weekly team summary",
                    "summary": f"{completed} of {len(tasks)} tasks in the current sample queue are complete.",
                },
                {
                    "title": "Coaching focus",
                    "summary": "Review pending sample tasks with each senior agent during the next team check-in.",
                },
            ],
        }

    if role == "demo_senior_agent":
        team = _TEAMS[0]
        agent_ids = {agent["id"] for agent in team["agents"]}
        tasks = [task for task in _TASKS if task["assignee_id"] in agent_ids]
        completed = sum(task["status"] == "Completed" for task in tasks)
        names = {agent["id"]: agent["name"] for agent in team["agents"]}
        activities = [
            activity
            for activity in _ACTIVITIES
            if activity["actor_id"] == team["senior_id"]
            or activity["actor_id"] in agent_ids
        ]
        return {
            "label": "Synthetic assigned-team performance",
            "notice": "This view contains fictional data for your assigned demo team only.",
            "scope": "assigned_team",
            "profile": {"name": team["senior_name"], "title": "Senior Agent"},
            "metrics": [
                {"label": "Assigned agents", "value": len(agent_ids)},
                {"label": "Tasks completed", "value": completed},
                {"label": "Tasks in progress", "value": sum(task["status"] == "In progress" for task in tasks)},
                {
                    "label": "Team completion rate",
                    "value": round(completed / len(tasks) * 100),
                    "unit": "%",
                },
            ],
            "team_members": _member_payload(team)[1:],
            "tasks": _task_payload(tasks, names),
            "task_analytics": _status_counts(tasks),
            "productivity": _PRODUCTIVITY,
            "activities": activities,
            "reports": [
                {
                    "title": "Assigned-team progress",
                    "summary": f"{completed} of {len(tasks)} sample tasks are complete across {len(agent_ids)} assigned agents.",
                },
                {
                    "title": "Next review",
                    "summary": "Check the in-progress duplicate-notification review and the pending merchant follow-up.",
                },
            ],
        }

    agent_id = "agent-1"
    agent = agent_by_id[agent_id]
    tasks = [task for task in _TASKS if task["assignee_id"] == agent_id]
    completed = sum(task["status"] == "Completed" for task in tasks)
    activities = [
        activity for activity in _ACTIVITIES if activity["actor_id"] == agent_id
    ]
    return {
        "label": "Synthetic personal performance",
        "notice": "This view contains fictional data for your demo profile only.",
        "scope": "personal",
        "profile": {"name": agent["name"], "title": "Agent"},
        "metrics": [
            {"label": "Assigned tasks", "value": len(tasks)},
            {"label": "Tasks completed", "value": completed},
            {"label": "Tasks in progress", "value": sum(task["status"] == "In progress" for task in tasks)},
            {"label": "Personal completion rate", "value": agent["completion_rate"], "unit": "%"},
        ],
        "team_members": [],
        "tasks": _task_payload(tasks, {agent_id: agent["name"]}),
        "task_analytics": _status_counts(tasks),
        "productivity": _AGENT_PRODUCTIVITY,
        "activities": activities,
        "reports": [
            {
                "title": "Personal performance summary",
                "summary": f"{completed} of {len(tasks)} assigned sample tasks are complete; personal quality score is {agent['completion_rate']}%.",
            },
            {
                "title": "Next action",
                "summary": "Continue the duplicate-notification review and document the next step before closing the case.",
            },
        ],
    }


@router.get("/dashboard")
async def dashboard(user: dict = Depends(require("view_demo"))):
    if user["role"] not in _DEMO_ROLES:
        raise HTTPException(status_code=403, detail="Permission denied")
    return _dashboard(user["role"])

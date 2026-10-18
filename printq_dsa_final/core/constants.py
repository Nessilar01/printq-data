ROLE_ADMIN = "admin"
ROLE_FREE = "free"
ROLE_PRO = "pro"
ROLES = (ROLE_ADMIN, ROLE_FREE, ROLE_PRO)


PLAN_FREE = "free"
PLAN_PRO = "pro"


PLAN_FEATURES = {
    PLAN_FREE: [
        "Upload .STL files and get an instant quote",
        "Order on the house farm or any farm storefront",
        "Track queue position and ETA",
        "Up to 3 active orders at once",
        "Files up to 25 MB",
    ],
    PLAN_PRO: [
        "Everything in Free",
        "Your own farm workspace + public storefront",
        "Register up to 10 printers",
        "Custom rate per minute and material surcharges",
        "Queue board: insert, cancel and delete jobs",
        "Material report and job search",
        "Up to 20 active orders, files up to 100 MB",
    ],
}


MATERIALS = ("PLA", "PETG", "ABS")
DEFAULT_RATE_PER_MIN_THB = 3
DEFAULT_SURCHARGES_THB = {"PLA": 20, "PETG": 35, "ABS": 30}


JOB_QUOTED = "quoted"
JOB_AWAITING_PAYMENT = "awaiting_payment"
JOB_QUEUED = "queued"
JOB_PRINTING = "printing"
JOB_DONE = "done"
JOB_CANCELLED = "cancelled"
JOB_STATUSES = (JOB_QUOTED, JOB_AWAITING_PAYMENT, JOB_QUEUED, JOB_PRINTING, JOB_DONE, JOB_CANCELLED)

JOB_ACTIVE = (JOB_AWAITING_PAYMENT, JOB_QUEUED, JOB_PRINTING)


PRINTER_IDLE = "idle"
PRINTER_PRINTING = "printing"
PRINTER_OFFLINE = "offline"
PRINTER_STATUSES = (PRINTER_IDLE, PRINTER_PRINTING, PRINTER_OFFLINE)


SUB_ACTIVE = "active"
SUB_CANCELED = "canceled"
SUB_EXPIRED = "expired"
SUB_STATUSES = (SUB_ACTIVE, SUB_CANCELED, SUB_EXPIRED)


TX_SUBSCRIPTION = "subscription"
TX_PRINT_ORDER = "print_order"
TX_REFUND = "refund"
TX_TYPES = (TX_SUBSCRIPTION, TX_PRINT_ORDER, TX_REFUND)

TX_PENDING = "pending"
TX_PAID = "paid"
TX_FAILED = "failed"
TX_EXPIRED = "expired"
TX_REFUNDED = "refunded"
TX_STATUSES = (TX_PENDING, TX_PAID, TX_FAILED, TX_EXPIRED, TX_REFUNDED)


ALLOWED_EXTENSIONS = (".stl", ".3mf")
MAX_DURATION_MIN = 3000


LAYER_HEIGHTS_MM = (0.12, 0.20, 0.28)
DEFAULT_LAYER_HEIGHT_MM = 0.20
MIN_INFILL_PCT = 0
MAX_INFILL_PCT = 100
DEFAULT_INFILL_PCT = 20
INFILL_PATTERNS = ("grid", "lines", "honeycomb", "gyroid")
DEFAULT_INFILL_PATTERN = "grid"

QUALITY_PRESETS = ("economy", "balanced", "strong", "fine")

PRESET_LABELS = {"economy": "Economical", "balanced": "Balanced", "strong": "Strong", "fine": "Detailed"}
PRESET_DEFAULTS = {
    "economy": dict(layer_height_mm=0.28, infill_density_pct=10, infill_pattern="lines", support_enabled=False),

    "balanced": dict(layer_height_mm=0.20, infill_density_pct=20, infill_pattern="grid", support_enabled=False),

    "strong": dict(layer_height_mm=0.20, infill_density_pct=50, infill_pattern="honeycomb", support_enabled=True),

    "fine": dict(layer_height_mm=0.12, infill_density_pct=25, infill_pattern="gyroid", support_enabled=True),
}


SHELL_VOLUME_FRACTION = 0.25
SUPPORT_VOLUME_FACTOR = 0.15
PATTERN_TIME_FACTOR = {"lines": 0.95, "grid": 1.00, "honeycomb": 1.05, "gyroid": 1.10}
REFERENCE_LAYER_HEIGHT_MM = DEFAULT_LAYER_HEIGHT_MM
MATERIAL_DENSITY_G_CM3 = {"PLA": 1.24, "PETG": 1.27, "ABS": 1.04}

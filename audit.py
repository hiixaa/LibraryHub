
from datetime import datetime
from functools import wraps


def audit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Run the original method first.
        result = method(self, *args, **kwargs)

        # Log only after the operation succeeds.
        if (
            hasattr(result, "member")
            and hasattr(result, "item")
        ):
            entry = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": method.__name__,
                "member": result.member.name,
                "item": result.item.title,
            }

            self.audit_log.append(entry)

        return result

    return wrapper

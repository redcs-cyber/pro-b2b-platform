import argparse

from .agents import GoodMoodEngine, classify_intent
from .ironman import format_ironman
from .telemetry import Telemetry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Jarvis assistant")
    parser.add_argument("--mode", choices=("local", "hybrid"), default="local")
    parser.add_argument("--visual", action="store_true")
    parser.add_argument("--ironman", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    telemetry = Telemetry()
    mood = GoodMoodEngine()
    message = f"Jarvis {args.mode} modunda hazır. GOODMOOD={mood.score}"
    telemetry.emit("startup", {"mode": args.mode, "visual": args.visual})
    print(format_ironman(message) if args.ironman else message)
    print(f"Intent örneği: {classify_intent('durum nedir')}")


if __name__ == "__main__":
    main()

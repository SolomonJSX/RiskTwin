import sys
import re
from pathlib import Path
from grpc_tools import protoc

# Ensure stdout/stderr handle UTF-8 properly on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main():
    # Service root: src/ml-engine
    root_dir = Path(__file__).resolve().parent

    # Proto definition: RiskTwin/proto
    proto_dir = (root_dir.parent.parent / "proto").resolve()
    proto_file = proto_dir / "ml_inference.proto"

    # Target directory: src/ml-engine/app/proto
    out_dir = root_dir / "app" / "proto"

    if not proto_file.exists():
        print(f"[!] Error: Proto file not found at: {proto_file}", file=sys.stderr)
        return 1

    # Ensure app/proto exists
    out_dir.mkdir(parents=True, exist_ok=True)

    args = [
        "grpc_tools.protoc",
        f"-I{proto_dir}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        str(proto_file),
    ]

    print(f"[*] Compiling {proto_file.name} -> {out_dir.relative_to(root_dir)}/ ...")
    exit_code = protoc.main(args)
    if exit_code != 0:
        print(f"[!] Proto compilation failed with code {exit_code}", file=sys.stderr)
        return exit_code

    # Automatically fix protoc absolute import bug: 'import ml_inference_pb2' -> 'from . import ml_inference_pb2'
    grpc_file = out_dir / "ml_inference_pb2_grpc.py"
    if grpc_file.exists():
        content = grpc_file.read_text(encoding="utf-8")
        fixed_content = re.sub(
            r"^import ml_inference_pb2 as",
            "from . import ml_inference_pb2 as",
            content,
            flags=re.MULTILINE,
        )
        grpc_file.write_text(fixed_content, encoding="utf-8")
        print("  [+] Fixed relative import in ml_inference_pb2_grpc.py")

    # Generate app/proto/__init__.py for clean imports
    init_file = out_dir / "__init__.py"
    init_content = (
        '"""Auto-generated Protobuf and gRPC modules."""\n\n'
        "from . import ml_inference_pb2\n"
        "from . import ml_inference_pb2_grpc\n\n"
        '__all__ = ["ml_inference_pb2", "ml_inference_pb2_grpc"]\n'
    )
    init_file.write_text(init_content, encoding="utf-8")
    print(f"  [+] Generated {init_file.relative_to(root_dir)}")

    print("[OK] Successfully generated gRPC modules in app/proto package!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
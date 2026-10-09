from cmk.agent_based.v2 import (  # type: ignore[reportMissingImports]
    AgentSection,
    CheckPlugin,
    Result,
    Service,
    State,
    StringTable,
)


def parse_dummy(string_table: StringTable) -> list[int]:
    return list(map(int, string_table.split(",")))


def discover_dummy(section):
    yield Service()


def check_dummy(section):
    yield Result(state=State.OK, summary="Dummy check is OK.")


agent_section_dummy = AgentSection(
    name="dummy",
    parse_function=parse_dummy,
)
check_plugin_dummy = CheckPlugin(
    name="dummy",
    sections=["dummy"],
    service_name="Dummy",
    discovery_function=discover_dummy,
    check_function=check_dummy,
)

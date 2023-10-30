_ctfd_cli_autocomplete() {
    local state

    _arguments \
        '1: :->mode' \
        '2: :->command' \
        '3: :->args' \
        && return 0

    case $state in
        (mode) _arguments '1:mode:(user team --ctfd-token --ctfd-instance)' ;;
        (command) _arguments '2:command:(list create delete update get)' ;;
    esac
}

compdef _ctfd_cli_autocomplete ctfd-cli
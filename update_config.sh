#!/bin/bash
while getopts ":f:o:n:" option; do
    case $option in
        f)
            file_name="$OPTARG"
            ;;
        o)
            old_text="$OPTARG"
            ;;
        n)
            new_text="$OPTARG"
            ;;
        *)
            echo "Usage: $0 [-f file_name] [-o query_text] [-n new_text]"
            exit 1
            ;;
    esac
done
sed -i "s/$old_text/$new_text/" $file_name
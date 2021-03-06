import re

from git_parser.processor.git_diff_hunk_processor import GitDiffHunk
from tools import logger


class GitPatchParser:
    """
    A parser for a patch which can computes useful information from it.
    """

    def __init__(self, commit_file):
        """
        Hunks are the sub parts of a patch which represent a single change in the patch.
        """
        self.__hunks = self.__extract_hunks(commit_file.patch)
        self.__commit_file_path = commit_file.path

    def calculate_updated_line_range(self, start_line, end_line):
        """
        Given an initial start line and end line, this function will calculate how those have changed for the file in
        response to the patch.
        """
        logger.get_logger().info("Caculating the updated line range for %s for lines %s to %s", str(self.__commit_file_path), str(start_line), str(end_line))

        updated_start_line = start_line
        updated_end_line = end_line

        for hunk in self.__hunks:

            if self.__is_hunk_before_line(hunk, start_line):
                updated_start_line += hunk.new_length - hunk.old_length
                updated_end_line += hunk.new_length - hunk.old_length

            elif self.__is_hunk_after_line(hunk, end_line):
                pass

            else:

                if self.__is_hunk_inside_line_range(hunk, start_line, end_line):
                    updated_end_line += hunk.new_length - hunk.old_length

                elif self.__is_hunk_overlapping_end(hunk, start_line, end_line):
                    updated_end_line += hunk.count_line_changed_before_inclusive(end_line)

                elif self.__is_hunk_overlapping_start(hunk, start_line, end_line):
                    updated_start_line += hunk.count_line_changed_before_inclusive(start_line)
                    updated_end_line += hunk.count_line_changed_after_exclusive(start_line) + \
                                        hunk.count_line_changed_before_inclusive(start_line)

        logger.get_logger().info("The updated line range for %s is %s to %s", str(self.__commit_file_path), str(updated_start_line), str(updated_end_line))

        return {
            "updated_start_line": updated_start_line,
            "updated_end_line": updated_end_line
        }

    def has_line_range_changed(self, start_line, end_line):
        """
        Whether the line range provided has been affected by the patch
        """
        logger.get_logger().info("Checking if line range has changed for %s, for lines %s to %s", str(str(self.__commit_file_path)), str(start_line), str(end_line))

        updated_line_range = self.calculate_updated_line_range(start_line, end_line)
        return not(updated_line_range["updated_start_line"] == start_line and updated_line_range["updated_end_line"] == end_line)

    def __extract_hunks(self, raw_patch):
        if not raw_patch:
            return []
        hunk_positions = [match.start() for match in re.finditer(GitDiffHunk.HUNK_HEADING_REGEX, raw_patch)]

        hunks = []
        for i in range(len(hunk_positions)):
            start_index = hunk_positions[i]
            end_index = len(raw_patch) if len(hunk_positions) == i + 1 else hunk_positions[i + 1]
            hunks.append(GitDiffHunk(raw_patch[start_index:end_index]))

        return hunks

    def __is_hunk_before_line(self, hunk, start_line):
        return self.__hunk_old_end_line(hunk) < start_line

    def __is_hunk_after_line(self, hunk, end_line):
        return end_line < hunk.old_start_line

    def __is_hunk_inside_line_range(self, hunk, start_line, end_line):
        return hunk.old_start_line > start_line and self.__hunk_old_end_line(hunk) < end_line

    def __is_hunk_overlapping_end(self, hunk, start_line, end_line):
        return hunk.old_start_line > start_line and self.__hunk_old_end_line(hunk) >= end_line

    def __is_hunk_overlapping_start(self, hunk, start_line, end_line):
        return hunk.old_start_line <= start_line and self.__hunk_old_end_line(hunk) < end_line

    def __hunk_old_end_line(self, hunk):
        return hunk.old_start_line + hunk.old_length - 1

from github import GithubException

from github_interface.wrappers.models.abstract_github_fs_node_model import AbstractGithubFSNode
from github_interface.wrappers.models.github_dir_model import GithubDirModel
from github_interface.wrappers.models.github_file_model import GithubFileModel
from utils.path_manipulator import PathManipulator


class GithubFSNodeFactory:
    """
    A factory for building file system nodes (files or directories) from raw data. A function is created to handle each
    of the different raw data to build from.
    """

    def create_from_github_get_contents(self, raw_fs_node):
        """
        Creates a file system node from a github get_contents request raw response.
        """

        if isinstance(raw_fs_node, list):
            raw_fs_node = self.__GithubDirectoryFactory().create_github_dir_from_github_get_contents(raw_fs_node)

        elif raw_fs_node.type == "file":
            raw_fs_node = self.__GithubFileFactory().create_github_file_from_github_get_contents(raw_fs_node)

        else:
            raise("This content type is not currently supported by the factories: " + str(raw_fs_node.type))

        return raw_fs_node

    def _create_from_github_get_contents_sub_fs_nodes(self, raw_fs_node):
        if raw_fs_node.type == "dir":
            fs_node = self.__GithubDirectoryFactory().create_github_dir_without_sub_fs_nodes_from_github_get_contents(raw_fs_node)

        else:
            fs_node = self.create_from_github_get_contents(raw_fs_node)

        return fs_node

    class __GithubDirectoryFactory:
        """
        Inner class factory for creating directories.
        """

        def create_github_dir_from_github_get_contents(self, raw_dirs):
            """
            Creates a directory from the github get contents request raw response.
            """

            return GithubDirModel(
                self.__extract_path_to_dir(raw_dirs[0].path),
                AbstractGithubFSNode.DIRECTORY_TYPE,
                self.__extract_sub_fs_nodes(raw_dirs)
            )

        def create_github_dir_without_sub_fs_nodes_from_github_get_contents(self, raw_fs_node):
            """
            Create a github directory without populating without sub file system nodes.
            """

            return GithubDirModel(
                raw_fs_node.path,
                AbstractGithubFSNode.DIRECTORY_TYPE
            )

        def __extract_path_to_dir(self, sub_fs_node_path):
            return PathManipulator().dissociate_dir_path_from_fs_node_name(sub_fs_node_path).dir_path

        def __extract_sub_fs_nodes(self, raw_dirs):
            return [GithubFSNodeFactory()._create_from_github_get_contents_sub_fs_nodes(raw_fs_node) for raw_fs_node in raw_dirs]

    class __GithubFileFactory:
        """
        Inner class factory for creating files.
        """

        def create_github_file_from_github_get_contents(self, raw_file):
            """
            Creates a file from the github get contents request raw response.
            """

            return GithubFileModel(
                raw_file.path,
                AbstractGithubFSNode.FILE_TYPE,
                self.__extract_decoded_content(raw_file)
            )

        def __extract_decoded_content(self, raw_file):
            try:
                if not raw_file:
                    return ""
                return raw_file.decoded_content.decode("utf-8")
            except GithubException:
                return "File is too large to be displayed (>1 MB in size)"
            except UnicodeDecodeError:
                return "Error decoding, 'utf-8' codec cannot decode"
            except AssertionError:
                return "Unsupported encoding"



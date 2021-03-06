<template>
  <div class="container mt-3">
    <div class="row card bg-light">
      <div class="card-header">Markdown</div>
      <div class="card-body">
        <div class="container">

          <div class="row mb-3">
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".modal">Add code reference</button>
            <button type="button" class="btn btn-success ml-2" @click="save">Save file</button>
          </div>

          <div class="row mb-3">
            <input type="email" class="form-control" placeholder="Document title" v-model="title">
          </div>

          <div class="row">
            <textarea class="form-control col-6 card" v-model="content" rows="20" ref="textarea"></textarea>

            <div class="col-6 card markdown-body">
              <MarkdownFile
                :name="title"
                :content="content"
                :refs="refs">
              </MarkdownFile>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Select lines</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>

          <div class="modal-body">
            <Browser
              @fileReference="setCurrentReference($event.fileReference)" />
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-dismiss="modal" @click="saveReference"
              v-if="this.currentReference.startLine && this.currentReference.endLine">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import Browser from "./elements/browser/Browser";
  import MarkdownFile from "./elements/MarkdownFile";

  export default {
    components: {
      Browser,
      MarkdownFile
    },

    data() {
      return {
        title: '',
        content: '',
        refs: [],
        currentReference: {}
      }
    },

    methods: {
      setCurrentReference(reference) {
        this.currentReference = reference;
      },

      saveReference() {
        // Hide the modal
        $('.modal').modal('hide');

        if (this.currentReference.startLine && this.currentReference.endLine) {

          let url = this._generateUrl(this.currentReference);

          this.$http.get(url).then(response => {
            const r = this.keysToCamel(response.body);

            this.currentReference.id = r.id;
            this.currentReference.code = r.code;

            // Save the reference and the content
            this.refs.push(this.currentReference);

            // Add the reference in the markdown
            this._addAtCursor(this.currentReference.id);

          }, error => {
            this.$bvToast.toast("An error has occurred while fetching github lines", {
              title: 'Error',
              autoHideDelay: 2000,
              variant: 'danger',
            });

          }).finally(() => {
            this.currentReference = {};
          });
        }
      },

      save() {
        if (!this.title) {
          this.$bvToast.toast("You must enter a title for your document", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          });
          return;
        }

        let references = [];

        for (const ref of this.refs) {
          references.push({
            'id': ref.id,
            'github_account_login': ref.githubAccountLogin,
            'repo_name': ref.repoName,
            'path': ref.path,
            'start_line': ref.startLine,
            'end_line': ref.endLine,
            'is_deleted': false
          })
        }

        let body = {
          'name': this.title,
          'content': this.content,
          'refs': references
        };

        this.$http.post('/api/' + this.$route.params.githubAccountLogin + '/save', body).then(response => {
          this.$bvToast.toast("File saved successfully", {
            title: 'Success',
            autoHideDelay: 2000,
            variant: 'success',
          });
        }, error => {
          this.$bvToast.toast("An error has occurred while saving", {
            title: 'Error',
            autoHideDelay: 2000,
            variant: 'danger',
          });
        });
      },

      _addAtCursor(referenceId) {
        const cursorPosition = this.$refs.textarea.selectionStart;

        const before = this.content.substring(0, cursorPosition);
        const after = this.content.substring(cursorPosition, this.content.length);
        const ref = this._generateRef(referenceId);

        this.content = before + ref + after;
      },

      _generateRef(referenceId) {
        return `[code-reference:${referenceId}]`;
      },

      _generateUrl(reference) {
        return '/api/' + this.$route.params.githubAccountLogin + '/lines?'
          + '&repo_name=' + encodeURIComponent(reference.repoName)
          + '&path=' + encodeURIComponent(reference.path)
          + '&start_line=' + encodeURIComponent(reference.startLine)
          + '&end_line=' + encodeURIComponent(reference.endLine);
      }
    }
  }
</script>

<style lang="scss">
</style>
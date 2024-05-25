<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const result = ref(null)

const onFileChange = (event) => {
  file.value = event.target.files[0]
}

const submitFile = async () => {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const response = await axios.post('http://localhost:5000/analyse_chat', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    result.value = JSON.stringify(response.data, null, 4)
  } catch (error) {
    console.error('Error uploading file:', error)
  }
}
</script>

<template>
  <div>
    <h1 class="text-center mb-4">Chat Analysis</h1>
    <div class="card mx-auto" style="max-width: 600px;">
      <div class="card-body">
        <div class="form-group mb-4">
          <label for="file" class="form-label">Upload Chat File:</label>
          <input type="file" class="form-control" id="file" @change="onFileChange">
        </div>
        <div class="d-flex justify-content-center">
          <button :disabled="!file" @click="submitFile" class="btn btn-primary btn-lg">Submit</button>
        </div>
      </div>
    </div>
    <div class="card mt-4 mx-auto" v-if="result" style="max-width: 600px;">
      <div class="card-body">
        <h2>Analysis Result</h2>
        <pre class="results">{{ result }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.results {
  white-space: pre-wrap;
}

.form-group {
  margin-bottom: 20px;
}
</style>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const file = ref(null)
const result = ref(null)
const loading = ref(false)
const plotUrls = ref([])

const onFileChange = (event) => {
  file.value = event.target.files[0]
}

const submitFile = async () => {
  if (!file.value) return

  const formData = new FormData()
  formData.append('file', file.value)

  loading.value = true

  try{
    const response = await fetch('http://127.0.0.1:5000/analyse_chat', {
      method: 'POST',
      body: formData
    })
    result.value = await response.json()
    console.log(result.value)
    loading.value = false
    const plotResponse = await fetch('http://127.0.0.1:5000/plot_chat', {
      method: 'POST',
      body: formData
    })
    plotUrls.value = await plotResponse.json()
    console.log(plotUrls.value)
  } catch {
    loading.value = false
    console.error('Failed to submit file')
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
    <div class="text-center" v-if="loading"> 
        <img src="../assets/ZKZg.gif" height="50" width="50">
    </div>
    <div class="card mt-4 mx-auto" v-if="result">
      <div class="card-body">
        <h2>Analysis Result</h2>
        <div v-for="analysis in result" :key="result">
          <div class="results" v-for="(user_analysis,key) in analysis" :key="user_analysis">
            <h3>User: {{key}}</h3>
            <p><em><b>Analysis:</b></em> {{user_analysis}}</p>
          </div>
        </div>
      </div>
    </div>
    <!-- <div class="card mt-4 mx-auto" v-if="plotUrls"> -->
    <div class="card mt-4 mx-auto" v-if="Object.keys(plotUrls).length > 0">
      <div class="card-body">
        <h2>Generated Plots</h2>
        <div v-for="(base64Image, index) in plotUrls" :key="index">
        <img :src="'data:image/png;base64,' + base64Image" alt="Plot" class="img-fluid mt-3"/>
        </div>
      </div>
    </div>
    <!-- </div> -->
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

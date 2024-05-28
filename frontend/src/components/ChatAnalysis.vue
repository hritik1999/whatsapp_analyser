<script setup>
import { ref } from 'vue'

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
          <label><a href="https://faq.whatsapp.com/1180414079177245/?cms_platform=android&helpref=platform_switcher&locale=eng">Click here </a>to see how to Export the chat. Please export without media.</label><br><br>
          <input type="file" class="form-control" id="file" @change="onFileChange">
        </div>
        <div class="d-flex justify-content-center">
          <button :disabled="!file" @click="submitFile" class="btn btn-primary btn-lg">Submit</button>
        </div>
      </div>
    </div>
    <div class="text-center" v-if="loading"> 
        <img src="../assets/ZKZg.gif" height="50" width="50">
        <p>Please wait a few minutes for the analysis to come!</p>
    </div>
    <div class="card mt-4 mx-auto" v-if="result">
      <div class="card-body">
        <h2>Analysis Result</h2>
        <div class="accordion" id="accordionExample">
          <div v-for="analysis in result" :key="result">
            <div class="accordion-item results" v-for="(user_analysis,key) in analysis" :key="user_analysis">
              <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                  <strong>User: {{key}} </strong>
                </button>
              </h2>
              <div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">
                <div class="accordion-body">
                  {{user_analysis}}
                </div>
              </div>
            </div>

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

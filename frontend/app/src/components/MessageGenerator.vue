<template>
  <div class="p-6 bg-white shadow-md rounded-lg max-w-lg mx-auto">
    <h2 class="text-xl font-bold mb-4">Generate a Message</h2>

    <input v-model="prompt" placeholder="Enter prompt" class="border rounded p-2 w-full mb-4" />
    <input v-model="recipientName" placeholder="Enter recipient name" class="border rounded p-2 w-full mb-4" />

    <button @click="generateMessage" class="bg-green-600 text-white px-4 py-2 rounded mb-4">
      Generate
    </button>

    <div v-if="message" class="mt-4 p-4 bg-gray-100 rounded">
      <div class="flex items-center justify-between mb-2">
        <p class="font-semibold">Generated Message:</p>
        <button @click="copyMessage" class="text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded">
          Copy
        </button>
      </div>
      <textarea v-model="message" class="w-full border p-2 rounded" rows="4"></textarea>
      <span v-if="copied" class="text-green-600 mt-2 block">Copied!</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "MessageGenerator",
  data() {
    return {
      prompt: "",
      recipientName: "",
      message: "",
      copied: false
    };
  },
  methods: {
    async generateMessage() {
      const response = await fetch("http://localhost:8000/generate-message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: this.prompt, name: this.recipientName })
      });
      if (response.ok) {
        const data = await response.json();
        this.message = data.generated_message.replace("{name}", this.recipientName || "there");
        this.copied = false;
      } else {
        this.message = "Failed to generate message.";
      }
    },
    copyMessage() {
      if (this.message) {
        navigator.clipboard.writeText(this.message).then(() => {
          this.copied = true;
          setTimeout(() => this.copied = false, 2000);
        });
      }
    }
  }
};
</script>

<style scoped>
/* Optional styling */
</style>

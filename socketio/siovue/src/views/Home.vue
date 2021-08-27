<template>
  <div class="home">
    <input v-model="message" placeholder="edit me">
    <button @click.prevent="senddata(message)">Send Message</button>
  </div>
</template>

<script>
// @ is an alias to /src
import io from "socket.io-client";

export default {
  name: 'Home',
  data() {
    return {
      message: "Hello World!",
      socket: null
    }
  },
  created() {
    this.socket = io.connect("http://10.1.1.113:44444");
    this.socket.on("message", fetcheddata => {
      console.log(fetcheddata);
    });
  },
  methods: {
    senddata(msg) {
      console.log("Sending: " + msg);
      this.socket.send(msg);
    }
  }
}
</script>

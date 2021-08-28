<template>
  <div class="home">
    <input v-model="message" placeholder="edit me">
    <button @click.prevent="senddata(message)">Send Message</button>
    <br />
    <textarea v-model="servermsgs"></textarea>
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
      socket: null,
      servermsgs: ""
    }
  },
  created() {
    this.socket = io.connect("http://192.168.1.157:44444");
    this.socket.on("connectevent", fetcheddata => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + fetcheddata['data'] + ": " + fetcheddata['sid'] + "\n";
    });
    this.socket.on("message", fetcheddata => {
      //console.log(fetcheddata);
      this.servermsgs = this.servermsgs + fetcheddata + "\n";
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

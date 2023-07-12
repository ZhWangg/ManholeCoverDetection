<template>
  <div class="container">
    <el-button type="danger" buttuon class="logout-button" @click="handleLogout"  icon="el-icon-warning">退出登录</el-button>
    <div class="title-section">
      <h1 class="title">井盖识别系统</h1>
    </div>
    <el-aside width="800px" class="aside-content">
      <el-card  class="card" shadow="always">
        <el-image  class="image" :src="getImageUrl()"></el-image>
        <div class="message-box" :width="card_width">
          <span v-bind:text="message">{{msg}}</span>
        </div>
      </el-card>
      <el-upload
        class="upload-demo"
        :action="uploadurl"
        :show-file-list="false"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        >
        <el-button type="primary" class="upload-btn" icon="el-icon-upload">上传图片</el-button>
      </el-upload>
      <el-card class="result-card" v-if="result"><span  v-bind:text="result" >识别的结果为：{{result}}</span></el-card>
    </el-aside>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      msg:"",
      uploadurl:"http://127.0.0.1:5000/UploadImg",
      result:"",
      card_width:"",
      card_height:""
    }
  },
  mounted() {
    document.title = '井盖识别系统';
  },created() {
    if (!this.$store.state.isAuthenticated) {
      this.$router.push('/');
    }
  },
  methods: {
    getImageUrl() {
      const filename = 'wzh.png'; // 图片名称
      const timestamp = Date.now(); // 时间戳或者UUID等唯一标识符
      return `http://127.0.0.1:5000/img/${filename}?v=${timestamp}`;
    },
    handleUploadSuccess(response, file) {
      this.msg=response.msg;
      this.result=response.predict_result
      this.card_width=response.card_width
      this.card_height=response.card_height
      console.log("这个是width"+this.card_width)
      console.log("这个是height"+this.card_height)

    },
    handleUploadError() {
      this.$message.error("上传失败");
    },
    handleLogout() {
      axios.post('http://127.0.0.1:5000/logout', {}, {
            withCredentials: true
        })
        .then(response => {
          if (response.data.message === 'User logged out successfully') {
            this.$message.success('登出成功');
            this.$router.push('/');
          } else {
            this.$message.error('登出失败');
          }
        })
        .catch(error => {
          this.$message.error('登出时发生错误');
        });
    },
  },
}
</script>

<style>

.logout-button {
  position: absolute;
  top: 20px;
  right: 20px;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  background-color: #d4ebf2;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  width: 100vw;
  min-height: 100vh;
  background-color: #d4ebf2;
}

.aside-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ffffff;
  margin: 20px;
  width: auto;
  max-width: 800px;
}

.title-section {
  width: 100%;
  padding: 20px 0;
  background-color: #d4ebf2;
  text-align: center;
}

.title {
  font-size: 3em;
  color: #007bff;
}

.card {
  width: auto;
  height: auto;
  margin: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
}

.image {
  width: 100%;
  height: auto;
}

.message-box {
  padding: 14px;
  background-color: #efefef;
  text-align: center;

}

.upload-demo {
  margin-top: 20px;
}

.upload-btn {
  font-size: 1em;
  color: white;
  background-color: #007bff;
  border-color: #007bff;
}

.result-card {
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 1.25em;
  font-weight: bold;
  color: #007bff;
}

</style>
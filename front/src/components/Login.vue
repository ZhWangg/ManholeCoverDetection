<template>
  <div class="login-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>井盖识别系统 登录</span>
      </div>
      <el-form :model="loginForm" status-icon :rules="rules" ref="loginForm" class="login-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username">
            <template slot="prepend">
              <i class="el-icon-user"></i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="loginForm.password">
            <template slot="prepend">
              <i class="el-icon-lock"></i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="form-buttons">
          <el-button type="primary" @click="handleSubmit('loginForm')">登录</el-button>
          <el-button type="primary" @click="$router.push('/register')">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名！', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码！', trigger: 'blur' }
        ]
      }
    }
  },mounted() {
    document.title = '井盖识别系统 登录';
  },
  methods: {
    handleSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post('http://127.0.0.1:5000/login', this.loginForm, {
            username: this.username,
            password: this.password
        }, {
            withCredentials: true
        })
            .then(response => {
              console.log(response);
              if (response.data.message) {
                this.$router.push('/home');
              }
            })
            .catch(error => {
              this.$message.error('用户名不存在或者密码错误！');
            });
        } else {
          return false;
        }
      });
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 50px 0;
}
.box-card {
  padding: 20px;
}
.login-form {
  margin-top: 20px;
}
.form-buttons {
  display: flex;
  justify-content: center;
}
</style>
<template>
  <div class="register-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>井盖识别系统 注册</span>
      </div>
      <el-form :model="registerForm" status-icon :rules="rules" ref="registerForm" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username">
            <template slot="prepend">
              <i class="el-icon-user"></i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="registerForm.password">
            <template slot="prepend">
              <i class="el-icon-lock"></i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="form-buttons">
          <el-button type="primary" @click="handleSubmit('registerForm')">注册</el-button>
          <el-button type="primary" @click="$router.push('/')">返回登录</el-button>
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
      registerForm: {
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
    document.title = '井盖识别系统 注册';
  },
  methods: {
    handleSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post('http://127.0.0.1:5000/register', this.registerForm,{
            username: this.username,
            password: this.password
        }, {
            withCredentials: true
        })
            .then(response => {
              console.log(response);
              if (response.data.message) {
                this.$router.push('/');
              }
            })
            .catch(error => {
              this.$message.error('该用户名已被注册！');
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
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 50px 0;
}
.box-card {
  padding: 20px;
}
.register-form {
  margin-top: 20px;
}
.form-buttons {
  display: flex;
  justify-content: center;
}
</style>
<template>
    <div >
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="真实姓名">
          <el-input style="width: 50%" v-model="realname"></el-input>
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input style="width: 50%" v-model="useremail"></el-input>
        </el-form-item>
        <el-form-item label="详细地址">
          <el-input style="width: 50%" v-model="useraddress"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">提交数据</el-button>
        </el-form-item>
      </el-form>
    </div>
</template>

<script>
    export default {
      name: "set",
      data() {
        return {
          realname: 'Tom',
          useremail: '2@qq.com',
          useraddress: 'xxx省xxx市xxx县'
        }
      },
      methods: {
        onSubmit() {
          console.log('submit!');
        }
      }
    }
</script>

<style scoped>

</style>

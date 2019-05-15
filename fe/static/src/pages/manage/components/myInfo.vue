<template>
    <div>
      <i class="el-icon-goods">用户信息</i>
      <hr/>
      <div id="main-contain">
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="用户名">
            <label>{{username}}</label>
          </el-form-item>
          <el-form-item label="真实姓名">
            <label>{{realname}}</label>
          </el-form-item>
          <el-form-item label="电子邮箱">
            <label>{{useremail}}</label>
          </el-form-item>
          <el-form-item label="详细地址">
            <label>{{useraddress}}</label>
          </el-form-item>
          <el-form-item label="在学课程">
            <label>{{classes_sum}}</label>
          </el-form-item>
          <el-form-item label="涉及领域">
            <label>{{category}}</label>
          </el-form-item>
        </el-form>
      </div>
    </div>
</template>

<script>
    export default {
      name: "myInfo",
      data() {
        return {
          username: '15591470327',
          realname: 'ak1996',
          useremail: '284951616@qq.com',
          useraddress: 'xxx省xxx市xxx县',
          classes_sum: 10,
          category: ['数学', '计算机', '金融'],
        }
      }
    }
</script>

<style lang="stylus" scoped>
</style>

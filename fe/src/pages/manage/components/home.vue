<template>
  <div class="main_div">
    <div class="manage_page">
      <el-row>
        <!--当前用户-->
        <el-col :span="6">
          <el-button disabled="disabled">当前用户:</el-button>
          {{current_user}}
        </el-col>
        <!--登出系统-->
        <el-col :span="2.5" style="float: right">
          <el-button  type="primary" @click="logout_sys()()">
            <i class="el-icon-close"></i>登出系统
          </el-button>
        </el-col>
        <!--间隔-->
        <el-col :span="0.3" style="float: right">&nbsp;&nbsp;</el-col>
        <!--管理员切换用户模块-->
        <el-col :span="2.5" style="float: right">
          <div v-if="is_admin">
            <el-button  type="primary" @click="switch_user()">
              <i class="el-icon-sort"></i>切换用户
            </el-button>
            <el-dialog
              title="切换用户"
              :visible.sync="dialogVisible"
              width="25%"
              :before-close="handleClose">
              <el-form>
                <el-form-item>
                  <el-select v-model="username" placeholder="请选择用户名">
                    <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="goto_user()">确认选择</el-button>
                </el-form-item>
              </el-form>
            </el-dialog>
          </div>
        </el-col>

      </el-row>
      <hr/>

      <el-row>
        <el-col :span="4">
          <el-menu :default-active="defaultActive" theme="dark" router>
            <el-menu-item index="manage"><i class="el-icon-menu"></i>首页</el-menu-item>
            <el-menu-item index="myInfo"><i class="el-icon-info"></i>我的信息</el-menu-item>
            <el-submenu index="2">
              <template slot="title"><i class="el-icon-goods"></i>我的学习</template>
              <el-menu-item index="myStudy"><i class="el-icon-document"></i>我的学习</el-menu-item>
            </el-submenu>
            <el-submenu index="3">
              <template slot="title"><i class="el-icon-goods"></i>我的课程</template>
              <el-menu-item index="myClass"><i class="el-icon-document"></i>我的课程</el-menu-item>
              <el-menu-item index="addClass"><i class="el-icon-circle-plus-outline"></i>新建课程</el-menu-item>
            </el-submenu>
            <el-submenu index="4">
              <template slot="title"><i class="el-icon-setting"></i>设置</template>
              <el-menu-item index="set"><i class="el-icon-setting"></i>设置</el-menu-item>
            </el-submenu>
            <el-submenu index="5">
              <template slot="title"><i class="el-icon-warning"></i>说明</template>
              <el-menu-item index="explain"><i class="el-icon-warning"></i>说明</el-menu-item>
            </el-submenu>
          </el-menu>
        </el-col>
        <el-col :span="20" style="height: 100%;overflow: auto;">
          <!--
          <keep-alive>
          </keep-alive>
          -->
          <router-view></router-view>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
    import $ from 'jquery'
    export default {
      name: 'home',
      created () {
        if(sessionStorage.getItem('super_token') == null)
          this.is_admin = false
        else {
          this.is_admin = true
        }
        this.current_user = this.getCookie_('username')
      },
      data() {
        return {
          is_admin: false,
          dialogVisible: false,
          username: '',
          current_user: '15591470327',
          options: [],
        }
      },
      computed: {
			  defaultActive: function(){
				  return this.$route.path.replace('/', '');
			  }
		  },
      methods:{
        switch_user() {
          //这里的this是vue中的this,当进入ajax之后,this就是ajax中的this,所以要先记录vue中的this
          var this_ = this
          var token = sessionStorage.getItem('super_token')
          $.ajax({
            type:"POST",
            async: false,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url:"http://localhost:8081/api/userlist",
            beforeSend: function(request) {
              request.setRequestHeader("Authorization", "JWT " +token);
            },
            success:function (data) {
              if (data['code'] == -400) {
                alert(data['message'])
              } else if (data['code'] == 0){
                this_.options = data['data']['users']
              }
            },
            error:function (e) {
              alert("500")
            }
          });
          this.dialogVisible = true
        },
        goto_user() {
          var request = {
            'username': this.username,
          }
          $.ajax({
            type:"POST",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(request),
            dataType: "json",
            url:"http://localhost:8081/api/super_switch",
            beforeSend: function(request) {
              request.setRequestHeader("Authorization", "JWT " + sessionStorage.getItem('super_token'))
            },
            success: function (data) {
              if (data['code'] == -400)
                alert(data['message'])
              else if (data['code'] == 0){
                alert(data['message'])
                var exdate = new Date()
                exdate.setDate(exdate.getDate() + (99) || 0)
                document.cookie = 'username' + '=' + escape(request.username) + ';expires=' + exdate.toGMTString()
                document.cookie = 'token' + '=' + escape(data['data']['access_token']) + ';expires=' + exdate.toGMTString()
                location.reload()
              }
            },
            error:function (e) {
              alert("服务器内部出错了，请稍等!!!");
            }
          });
          this.dialogVisible = false
        },
        getCookie_(key_str){
          if(document.cookie.length > 0) {
            var cStart = document.cookie.indexOf(key_str + '=')
            if(cStart != 1){
              cStart = cStart + key_str.length + 1
              var cEnd = document.cookie.indexOf(';', cStart)
              if(cEnd == -1){
                cEnd = document.cookie.length
              }
              var value_str = unescape(document.cookie.substring(cStart, cEnd))
              return value_str
            }
          } else {
            return ''
          }
        },
        logout_sys() {
          if(sessionStorage.getItem('super_token') != null)
            sessionStorage.removeItem('super_token')
          window.location.href = 'login.html'
        }
      }
    }
</script>

<style lang="less" scoped>
  .main_div {
    height: 100%;
    width: 100%;
    background: #8cc5ff;
  }
	.manage_page{
    width: 80%;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    background: #ffffff;
	}
</style>

<template>
  <div class="manage_page fillcontain">
		<el-row style="height: 100%;">
	  		<el-col :span="4"  style="min-height: 100%; background-color: #324057;">
				<el-menu :default-active="defaultActive" style="min-height: 100%;" theme="dark" router>
					<el-menu-item index="manage"><i class="el-icon-menu"></i>首页</el-menu-item>
          <el-menu-item index="myInfo"><i class="el-icon-info"></i>我的信息</el-menu-item>
					<el-submenu index="2">
						<template slot="title"><i class="el-icon-goods"></i>我的学习</template>
						<el-menu-item index="myStudy"><i class="el-icon-document"></i>我的学习</el-menu-item>
						<el-menu-item index="addStudy"><i class="el-icon-circle-plus-outline"></i>新建学习</el-menu-item>
					</el-submenu>
					<el-submenu index="3">
						<template slot="title"><i class="el-icon-goods"></i>我的课程</template>
						<el-menu-item index="myClass"><i class="el-icon-document"></i>我的课程</el-menu-item>
						<el-menu-item index="addClass"><i class="el-icon-circle-plus-outline"></i>新建课程</el-menu-item>
					</el-submenu>
					<el-submenu index="4">
						<template slot="title"><i class="el-icon-setting"></i>设置</template>
						<el-menu-item index="set">管理员设置</el-menu-item>
						<!-- <el-menu-item index="sendMessage">发送通知</el-menu-item> -->
					</el-submenu>
					<el-submenu index="5">
						<template slot="title"><i class="el-icon-warning"></i>说明</template>
						<el-menu-item index="explain">说明</el-menu-item>
					</el-submenu>
				</el-menu>
			</el-col>
			<el-col :span="20" style="height: 100%;overflow: auto;">
				<keep-alive>
				    <router-view></router-view>
				</keep-alive>
			</el-col>
		</el-row>
  </div>
</template>

<script>
    export default {
      name: 'home',
      computed: {
			  defaultActive: function(){
				  return this.$route.path.replace('/', '');
			  }
		  },
    }
</script>

<style lang="less" scoped>
	@import '../style/mixin';
	.manage_page{
	}
</style>

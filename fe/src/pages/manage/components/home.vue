<template>
  <div class="main_div">
  <div class="manage_page">
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

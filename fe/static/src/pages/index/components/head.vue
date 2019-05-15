<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick" type="card">
      <el-tab-pane label="主页" name="first">
        <h2>什么是在线教学?</h2>
        <p style="font-size: 14px">了解在线教学很简单，在线学习正在学习利用电子技术在传统教室之外访问教育课程。在大多数情况下，它指的是完全在线提供的课程，计划或学位。</p>
        <p style="font-size: 14px">有许多术语用于描述通过互联网在线提供的学习，包括远程教育，计算机化电子学习，在线学习，互联网学习等等。我们将电子教学定义为通过互联网专门提供给教授所在教室以外的其他课程。它不是通过DVD或CD-ROM，录像带或电视频道提供的课程。它具有互动性，您还可以与班级中的老师，教授或其他学生进行交流。有时它是现场直播，你可以“电子地”举手并实时互动，有时这是一个已经预先录制的讲座。总有一位老师或教授与您互动/沟通并对您的参与进行评分，你的作业和考试。电子学习已被证明是一种成功的培训方法，教育正在成为北卡罗来纳州许多公民的生活方式。</p>
        <div align="center">
          <img src="static/img/timg.jpeg" height="300"/>
        </div>
        <p style="font-size: 14px">在本平台上我们提供了丰富多样的课程资源，灵活自由的学习方式和学习分享方式，在这里人人都是学习者，同时人人也都是教学者。让我们来大致看一下吧！！！</p>
      </el-tab-pane>
      <el-tab-pane label="帮助" name="second">
        <p style="font-size: 14px">第一次来，还不知道怎么操作。</p>
        <p style="font-size: 14px">去登录注册看看吧！！！</p>
      </el-tab-pane>
      <el-tab-pane label="登录/注册" name="third" align="center">
        <p style="font-size: 14px">让我们开始吧---></p>
        <el-button type="primary" onclick="window.location='login.html'">登录/注册</el-button>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
    export default {
        name: "head",
        data() {
          return {
            activeName: 'first'
          };
        },
        methods: {
          handleClick(tab, event) {
            console.log(tab, event);
          }
        }
    }
</script>

<style scoped>

</style>

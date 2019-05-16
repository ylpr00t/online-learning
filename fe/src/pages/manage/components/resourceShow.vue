<template>
    <div>
      <!--head-->
      <div>
        <el-button type="primary" plain @click="back_()">
          <i class="el-icon-back"></i>去上一级
        </el-button>
      </div><hr/>

      <!--text-->
      <div v-if="resource_type == 1">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <p>{{resource_content}}</p>
        </div>
      </div>

      <!--pic-->
      <div v-if="resource_type == 2">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <img :src="resource_content" height="300"/>
        </div>
      </div>

      <!--video-->
      <div v-if="resource_type == 3">
        <div align="center">
          <span>{{resource_name}}</span><br/>
          <video :src="resource_content" controls="controls" width="600px" height="400px">
            您的浏览器不支持 video 标签。
          </video>
        </div>
      </div>

    </div>
</template>

<script>
    export default {
      name: "resourceShow",
      data() {
        return {
          classes_id: this.$route.params.classes_id,
          resource_name: this.$route.params.resource_name,
          resource_type: this.$route.params.resource_type,
          resource_content: this.$route.params.resource_content,
        }
      },
      methods: {
        back_() {
          this.$router.push({
            name: 'resourceInfo',
            params: {
              classes_id: this.classes_id
            }
          })
        }
      }
    }
</script>

<style scoped>

</style>

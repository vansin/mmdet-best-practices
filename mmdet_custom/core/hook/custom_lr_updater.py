from mmcv.runner.hooks import HOOKS, LrUpdaterHook


@HOOKS.register_module()
class CustomLrUpdaterHook(LrUpdaterHook):
    def __init__(self, gamma=0.8, **kwargs):
        self.gamma = gamma
        super(CustomLrUpdaterHook, self).__init__(**kwargs)

    def get_lr(self, runner, base_lr):
        progress = runner.epoch if self.by_epoch else runner.iter
        return base_lr * self.gamma**progress

    def before_train_epoch(self, runner):
        # overwrite the before_train_epoch
        return

    def before_train_iter(self, runner):
        # overwrite the before_train_epoch
        return

    def after_train_epoch(self, runner):
        if self.warmup_iters is None:
            epoch_len = len(runner.data_loader)
            self.warmup_iters = self.warmup_epochs * epoch_len

        if not self.by_epoch:
            return

        self.regular_lr = self.get_regular_lr(runner)
        self._set_lr(runner, self.regular_lr)

    def after_train_iter(self, runner):
        cur_iter = runner.iter
        if not self.by_epoch:
            self.regular_lr = self.get_regular_lr(runner)
            if self.warmup is None or cur_iter >= self.warmup_iters:
                self._set_lr(runner, self.regular_lr)
            else:
                warmup_lr = self.get_warmup_lr(cur_iter)
                self._set_lr(runner, warmup_lr)
        elif self.by_epoch:
            if self.warmup is None or cur_iter > self.warmup_iters:
                return
            elif cur_iter == self.warmup_iters:
                self._set_lr(runner, self.regular_lr)
            else:
                warmup_lr = self.get_warmup_lr(cur_iter)
                self._set_lr(runner, warmup_lr)


@HOOKS.register_module()
class NotionLrUpdaterHook(LrUpdaterHook):
    def __init__(self,
                 page_id='e4611a15caec4eca942e2011c1f7c6de',
                 notion_token='',
                 **kwargs):

        from notion_client import Client
        self.notion = Client(auth=notion_token)
        self.api_url = 'https://api.notion.com/v1/pages/' + page_id
        super(NotionLrUpdaterHook, self).__init__(**kwargs)

    def get_lr(self, runner, base_lr):

        infos = self.notion.request(self.api_url, 'GET')
        # progress = runner.epoch if self.by_epoch else runner.iter
        return infos['properties']['lr']['number']

    # def before_train_epoch(self, runner):
    #     # overwrite the before_train_epoch
    #     return

    # def before_train_iter(self, runner):
    #     # overwrite the before_train_epoch
    #     return

    # def after_train_epoch(self, runner):
    #     if self.warmup_iters is None:
    #         epoch_len = len(runner.data_loader)
    #         self.warmup_iters = self.warmup_epochs * epoch_len

    #     if not self.by_epoch:
    #         return

    #     self.regular_lr = self.get_regular_lr(runner)
    #     self._set_lr(runner, self.regular_lr)

    # def after_train_iter(self, runner):
    #     cur_iter = runner.iter
    #     if not self.by_epoch:
    #         self.regular_lr = self.get_regular_lr(runner)
    #         if self.warmup is None or cur_iter >= self.warmup_iters:
    #             self._set_lr(runner, self.regular_lr)
    #         else:
    #             warmup_lr = self.get_warmup_lr(cur_iter)
    #             self._set_lr(runner, warmup_lr)
    #     elif self.by_epoch:
    #         if self.warmup is None or cur_iter > self.warmup_iters:
    #             return
    #         elif cur_iter == self.warmup_iters:
    #             self._set_lr(runner, self.regular_lr)
    #         else:
    #             warmup_lr = self.get_warmup_lr(cur_iter)
    #             self._set_lr(runner, warmup_lr)

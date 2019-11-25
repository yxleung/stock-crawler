import os


def query_cpu():
    if os.path.isfile('/sys/fs/cgroup/cpu/cpu.cfs_quota_us'):
        cpu_quota = int(open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us').read().rstrip())
    # print(cpu_quota) # Not useful for AWS Batch based jobs as result is -1, but works on local linux systems
    if cpu_quota != -1 and os.path.isfile('/sys/fs/cgroup/cpu/cpu.cfs_period_us'):
        cpu_period = int(open('/sys/fs/cgroup/cpu/cpu.cfs_period_us').read().rstrip())
        avail_cpu = int(
            cpu_quota / cpu_period)  # Divide quota by period and you should get num of allotted CPU to the container, rounded down if fractional.
    elif os.path.isfile('/sys/fs/cgroup/cpu/cpu.shares'):
        cpu_shares = int(open('/sys/fs/cgroup/cpu/cpu.shares').read().rstrip())
        # print(cpu_shares) # For AWS, gives correct value * 1024.
        avail_cpu = int(cpu_shares / 1024)
    return avail_cpu

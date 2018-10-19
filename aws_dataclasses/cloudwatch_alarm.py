from datetime import datetime
from typing import Dict, List

import arrow
from dataclasses import dataclass, InitVar, field

from aws_dataclasses.base import GenericDataClass, EventClass


@dataclass
class CloudWatchAlarmTrigger(GenericDataClass):
    MetricName: InitVar[str] = field(repr=False)
    Namespace: InitVar[str] = field(repr=False)
    StatisticType: InitVar[str] = field(repr=False)
    Statistic: InitVar[str] = field(repr=False)
    Dimensions: InitVar[List[Dict]] = field(repr=False)
    Period: InitVar[int] = field(repr=False)
    EvaluationPeriods: InitVar[int] = field(repr=False)
    ComparisonOperator: InitVar[str] = field(repr=False)
    Threshold: InitVar[float] = field(repr=False)
    TreatMissingData: InitVar[str] = field(repr=False)
    EvaluateLowSampleCountPercentile: InitVar[str] = field(repr=False, default=None)
    Unit: InitVar[str] = field(repr=False, default=None)
    metric_name: str = field(init=False)
    namespace: str = field(init=False)
    statistic_type: str = field(init=False)
    statistic: str = field(init=False)
    unit: str = field(init=False)
    dimensions: List[Dict] = field(init=False)
    period: str = field(init=False)
    evaluation_periods: str = field(init=False)
    comparison_operator: str = field(init=False)
    threshold: str = field(init=False)
    treat_missing_data: str = field(init=False)
    evaluate_low_samplecount_percentile: str = field(init=False)


    def __post_init__(self, MetricName: str, Namespace: str, StatisticType: str, Statistic: str, Dimensions: List[Dict],
                      Period: int, EvaluationPeriods: int, ComparisonOperator: str, Threshold: float,
                      TreatMissingData: str, EvaluateLowSampleCountPercentile: str, Unit: str):
        self.metric_name = MetricName
        self.namespace = Namespace
        self.statistic_type = StatisticType
        self.statistic = Statistic
        self.unit = Unit
        self.dimensions = Dimensions
        self.period = Period
        self.evaluation_periods = EvaluationPeriods
        self.comparison_operator = ComparisonOperator
        self.threshold = Threshold
        self.treat_missing_data = TreatMissingData
        self.evaluate_low_samplecount_percentile = EvaluateLowSampleCountPercentile


@dataclass
class CloudWatchAlarm(EventClass):
    AlarmName: InitVar[str] = field(repr=False)
    AlarmDescription: InitVar[str] = field(repr=False)
    AWSAccountId: InitVar[str] = field(repr=False)
    NewStateValue: InitVar[str] = field(repr=False)
    NewStateReason: InitVar[str] = field(repr=False)
    StateChangeTime: InitVar[str] = field(repr=False)
    Region: InitVar[str] = field(repr=False)
    OldStateValue: InitVar[str] = field(repr=False)
    Trigger: InitVar[Dict] = field(repr=False)
    alarm_name: str = field(init=False)
    alarm_description: str = field(init=False)
    aws_account_id: str = field(init=False)
    new_state_value: str = field(init=False)
    old_state_value: str = field(init=False)
    new_state_reason: str = field(init=False)
    state_change_time: datetime = field(init=False)
    region: str = field(init=False)
    trigger: CloudWatchAlarmTrigger = field(init=False)

    def __post_init__(self, AlarmName: str, AlarmDescription: str, AWSAccountId: str, NewStateValue: str,
                      NewStateReason: str, StateChangeTime: str, Region: str, OldStateValue: str, Trigger: Dict):
        self.alarm_name = AlarmName
        self.alarm_description = AlarmDescription
        self.aws_account_id = AWSAccountId
        self.new_state_value = NewStateValue
        self.new_state_reason = NewStateReason
        self.old_state_value = OldStateValue
        self.region = Region
        self.state_change_time = arrow.get(StateChangeTime).datetime
        self.trigger = CloudWatchAlarmTrigger.from_json(Trigger)

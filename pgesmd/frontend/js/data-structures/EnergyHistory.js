// EnergyHistory :: f (a) -> f (b)
export class EnergyHistory {
  constructor(database, partitionOptions, interval, passiveUse = null) {
    this.database = database;
    this.partitionOptions = partitionOptions;
    this.passiveUse = passiveUse ? passiveUse : calculatePassiveUse(database);
    this._graphData = getDataset(database)({
      start: interval.start,
      end: interval.end,
    });
    this.data = {
      start: interval.start,
      end: interval.end,
      intervalSize: findMaxResolution(
        differenceInMilliseconds(interval.start, interval.end)
      ),
      datasets: [
        {
          label: "Energy Consumption",
          type: "bar",
          data: this._graphData.toJS(),
          backgroundColor: makeColorsArray(partitionOptions)(
            this._graphData
          ).toArray(),
        },
        {
          label: "Passive Consumption",
          type: "line",
          data: this.passiveUse,
        },
      ],
    };
    this.windowData = {
      windowSize: intervalToWindow(this.data.intervalSize),
      windowSum: sum(extract("y")(this._graphData)),
      partitionSums: sumPartitions(partitionOptions)(this._graphData),
    };
  }

  prev() {
    return new EnergyHistory(
      this.database,
      this.partitionOptions,
      {
        start: sub(this.data.start, one(this.windowData.windowSize)),
        end: sub(this.data.end, one(this.windowData.windowSize)),
      },
      (this.passiveUse = this.passiveUse)
    );
  }

  next() {
    return new EnergyHistory(
      this.database,
      this.partitionOptions,
      {
        start: add(this.data.start, one(this.windowData.windowSize)),
        end: add(this.data.end, one(this.windowData.windowSize)),
      },
      (this.passiveUse = this.passiveUse)
    );
  }

  setWindow(interval) {
    return new EnergyHistory(
      this.database,
      this.partitionOptions,
      {
        start: startOf(interval)(this.data.start),
        end: endOf(interval)(this.data.start),
      },
      (this.passiveUse = this.passiveUse)
    );
  }
}